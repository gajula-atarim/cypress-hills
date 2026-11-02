// Cypress Hills — swap the Contact page owners' photo for the sharper version (run via Atarim execute-php).
// Uploads design/images/cypress-hills-owners-hd.jpg from the pinned commit (once) and points the Image
// widget with class "ch-owner-photo" at it. Same framing as before; nothing else on the page changes.
// When the client's original photo arrives, export it the same way and re-run with a new file name.
$ref = 'REF'; // replaced with the commit SHA when run
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$page = get_page_by_path( 'contact', OBJECT, 'page' );
if ( ! $page ) {
	throw new Exception( 'contact page not found' );
}
$alt = 'The owners of Cypress Hills Landscaping';
$ex  = get_posts( array( 'post_type' => 'attachment', 'name' => 'cypress-hills-owners-hd', 'post_status' => 'any', 'numberposts' => 1 ) );
if ( $ex ) {
	$aid = $ex[0]->ID;
} else {
	$tmp = download_url( 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/' . $ref . '/design/images/cypress-hills-owners-hd.jpg', 30 );
	if ( is_wp_error( $tmp ) ) {
		throw new Exception( 'download failed: ' . $tmp->get_error_message() );
	}
	$aid = media_handle_sideload( array( 'name' => 'cypress-hills-owners-hd.jpg', 'tmp_name' => $tmp ), $page->ID, 'Cypress Hills owners' );
	if ( is_wp_error( $aid ) ) {
		@unlink( $tmp );
		throw new Exception( 'upload failed: ' . $aid->get_error_message() );
	}
}
update_post_meta( $aid, '_wp_attachment_image_alt', $alt );

$n    = 0;
$walk = function ( $els ) use ( &$walk, $aid, $alt, &$n ) {
	foreach ( $els as $i => $el ) {
		$c = isset( $el['settings']['_css_classes'] ) ? $el['settings']['_css_classes'] : '';
		if ( isset( $el['widgetType'] ) && 'image' === $el['widgetType'] && preg_match( '/(^|\s)ch-owner-photo(\s|$)/', $c ) ) {
			$els[ $i ]['settings']['image'] = array( 'id' => $aid, 'url' => wp_get_attachment_url( $aid ), 'alt' => $alt, 'source' => 'library' );
			$n++;
		}
		if ( ! empty( $el['elements'] ) ) {
			$els[ $i ]['elements'] = $walk( $el['elements'] );
		}
	}
	return $els;
};
$doc  = \Elementor\Plugin::$instance->documents->get( $page->ID, false );
$data = $walk( $doc->get_elements_data() );
if ( 1 !== $n ) {
	throw new Exception( 'expected 1 owners photo, found ' . $n );
}
$doc->save( array( 'elements' => $data ) );
\Elementor\Plugin::$instance->files_manager->clear_cache();
echo wp_json_encode( array( 'attachment' => $aid, 'url' => wp_get_attachment_url( $aid ) ) );
