// Cypress Hills — put the original brand-kit photos back on the 7 Home banner slides and drop the
// per-slide framing (ch-fit / ch-pos-top). Only the slide image widgets change.
$orig = array( 61, 57, 58, 59, 64, 60, 63 ); // aerial-estate, pool, armour-stone, putting-green, golf-course, outdoor-kitchen, night-lighting
$home = (int) get_option( 'page_on_front' );
$doc  = \Elementor\Plugin::$instance->documents->get( $home, false );
$n    = 0;
$walk = function ( $els ) use ( &$walk, &$n, $orig ) {
	foreach ( $els as $k => $el ) {
		$s   = isset( $el['settings'] ) ? $el['settings'] : array();
		$cls = isset( $s['_css_classes'] ) ? $s['_css_classes'] : '';
		if ( isset( $el['widgetType'] ) && 'image' === $el['widgetType'] && preg_match( '/(^|\s)ch-slide-img(\s|$)/', $cls ) ) {
			$id = $orig[ $n ];
			if ( ! wp_get_attachment_url( $id ) ) {
				throw new Exception( 'missing attachment ' . $id );
			}
			$s['image'] = array( 'id' => $id, 'url' => wp_get_attachment_url( $id ), 'alt' => get_post_meta( $id, '_wp_attachment_image_alt', true ), 'source' => 'library' );
			$s['_css_classes'] = implode( ' ', array_diff( preg_split( '/\s+/', trim( $cls ) ), array( 'ch-fit', 'ch-pos-top' ) ) );
			unset( $s['_background_background'], $s['_background_image'] );
			$els[ $k ]['settings'] = $s;
			$n++;
		}
		if ( ! empty( $el['elements'] ) ) {
			$els[ $k ]['elements'] = $walk( $el['elements'] );
		}
	}
	return $els;
};
$data = $walk( $doc->get_elements_data() );
if ( 7 !== $n ) {
	throw new Exception( 'expected 7 banner slides, found ' . $n );
}
$doc->save( array( 'elements' => $data ) );
\Elementor\Plugin::$instance->files_manager->clear_cache();
echo wp_json_encode( array( 'slides' => $n, 'images' => $orig ) );
