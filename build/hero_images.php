// Cypress Hills — swap the Home banner slide photos in place (run via Atarim execute-php).
// Only the image of each listed slide changes; text, buttons, links and every other section stay as they are.
// Slides are matched in order by their "ch-slide-img" image widget. null = leave that slide unchanged.
$base   = 'https://cypress-hills.wsdfy.com/wp-content/uploads/2026/10/';
$photos = array(
	'mike-2.jpeg',          // 1 Transforming Landscapes, One Project at a Time
	'mike17-rotated.jpeg',  // 2 The pool and the yard, built as one.
	'mike19-rotated.jpeg',  // 3 Stone walls set by our own crew and machines.
	'mike-golf.jpeg',       // 4 Your own short game, steps from the house.
	'mike16-scaled.jpeg',   // 5 Greens and bunkers shaped for real courses.
	'mike3.jpeg',           // 6 Kitchens, cabanas and fire for long evenings.
	null,                   // 7 A yard that works after dark. (photo to come)
);
$ids = array();
foreach ( $photos as $i => $file ) {
	if ( null === $file ) {
		continue;
	}
	$id = attachment_url_to_postid( $base . $file );
	if ( ! $id ) {
		throw new Exception( 'not in media library: ' . $file );
	}
	$ids[ $i ] = array( 'id' => $id, 'url' => wp_get_attachment_url( $id ), 'alt' => get_post_meta( $id, '_wp_attachment_image_alt', true ) );
}
$home = (int) get_option( 'page_on_front' );
$doc  = \Elementor\Plugin::$instance->documents->get( $home, false );
$data = $doc->get_elements_data();
$n    = 0;
$done = array();
$walk = function ( $els ) use ( &$walk, &$n, $ids, &$done ) {
	foreach ( $els as $k => $el ) {
		$cls = isset( $el['settings']['_css_classes'] ) ? $el['settings']['_css_classes'] : '';
		if ( isset( $el['widgetType'] ) && 'image' === $el['widgetType'] && preg_match( '/(^|\s)ch-slide-img(\s|$)/', $cls ) ) {
			if ( isset( $ids[ $n ] ) ) {
				$els[ $k ]['settings']['image'] = array(
					'id'     => $ids[ $n ]['id'],
					'url'    => $ids[ $n ]['url'],
					'alt'    => $ids[ $n ]['alt'],
					'source' => 'library',
				);
				$done[ $n + 1 ] = $ids[ $n ]['id'];
			}
			$n++;
		}
		if ( ! empty( $el['elements'] ) ) {
			$els[ $k ]['elements'] = $walk( $el['elements'] );
		}
	}
	return $els;
};
$data = $walk( $data );
if ( 7 !== $n ) {
	throw new Exception( 'expected 7 banner slides, found ' . $n );
}
$doc->save( array( 'elements' => $data ) );
\Elementor\Plugin::$instance->files_manager->clear_cache();
echo wp_json_encode( array( 'slides_found' => $n, 'replaced' => $done ) );
