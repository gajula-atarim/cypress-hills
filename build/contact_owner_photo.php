// Cypress Hills — add the owners' photo to the Contact page (run via Atarim execute-php).
// Uploads design/images/cypress-hills-owners.jpg from the pinned commit (once), then inserts one Image
// widget right after the "Service Area" card in the live page. Nothing else on the page is touched.
// Re-running is safe: the upload is reused and the widget is not added twice.
$ref = 'REF'; // replaced with the commit SHA when run (first run: be6ecbe)
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$page = get_page_by_path( 'contact', OBJECT, 'page' );
if ( ! $page ) {
	throw new Exception( 'contact page not found' );
}
$alt = 'The owners of Cypress Hills Landscaping';
$ex  = get_posts( array( 'post_type' => 'attachment', 'name' => 'cypress-hills-owners', 'post_status' => 'any', 'numberposts' => 1 ) );
if ( $ex ) {
	$aid = $ex[0]->ID;
} else {
	$tmp = download_url( 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/' . $ref . '/design/images/cypress-hills-owners.jpg', 30 );
	if ( is_wp_error( $tmp ) ) {
		throw new Exception( 'download failed: ' . $tmp->get_error_message() );
	}
	$aid = media_handle_sideload( array( 'name' => 'cypress-hills-owners.jpg', 'tmp_name' => $tmp ), $page->ID, 'Cypress Hills owners' );
	if ( is_wp_error( $aid ) ) {
		@unlink( $tmp );
		throw new Exception( 'upload failed: ' . $aid->get_error_message() );
	}
}
update_post_meta( $aid, '_wp_attachment_image_alt', $alt );

$doc  = \Elementor\Plugin::$instance->documents->get( $page->ID, false );
$data = $doc->get_elements_data();
$has  = function ( $el, $cls ) {
	$c = isset( $el['settings']['_css_classes'] ) ? $el['settings']['_css_classes'] : ( isset( $el['settings']['css_classes'] ) ? $el['settings']['css_classes'] : '' );
	return (bool) preg_match( '/(^|\s)' . preg_quote( $cls, '/' ) . '(\s|$)/', $c );
};
$photo = array(
	'id'         => substr( md5( 'ch-owner-photo' ), 0, 7 ),
	'elType'     => 'widget',
	'widgetType' => 'image',
	'isInner'    => false,
	'settings'   => array(
		'image'        => array( 'id' => $aid, 'url' => wp_get_attachment_url( $aid ), 'alt' => $alt, 'source' => 'library' ),
		'image_size'   => 'full',
		'width'        => array( 'unit' => '%', 'size' => 100, 'sizes' => array() ),
		'_css_classes' => 'ch-media ch-owner-photo',
	),
	'elements'   => array(),
);
$state = array( 'found' => false, 'exists' => false );
$walk  = function ( $els ) use ( &$walk, $has, $photo, &$state ) {
	$out = array();
	foreach ( $els as $el ) {
		if ( $has( $el, 'ch-owner-photo' ) ) {
			$state['exists'] = true;
		}
		if ( ! empty( $el['elements'] ) ) {
			$el['elements'] = $walk( $el['elements'] );
		}
		$out[] = $el;
		if ( $has( $el, 'ch-area-card' ) ) {
			$state['found'] = true;
			$out[]          = $photo;
		}
	}
	return $out;
};
$new = $walk( $data );
if ( ! $state['found'] ) {
	throw new Exception( 'Service Area card not found' );
}
if ( ! $state['exists'] ) {
	$doc->save( array( 'elements' => $new ) );
}

// Theme CSS from the same commit (adds the .ch-owner-photo rules).
$rel = 'assets/css/cypress-hills.css';
$r   = wp_remote_get( 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/' . $ref . '/wp-content/themes/hello-elementor-child/' . $rel, array( 'timeout' => 30 ) );
if ( is_wp_error( $r ) || 200 !== wp_remote_retrieve_response_code( $r ) ) {
	throw new Exception( 'css fetch failed' );
}
file_put_contents( get_stylesheet_directory() . '/' . $rel, wp_remote_retrieve_body( $r ) );
\Elementor\Plugin::$instance->files_manager->clear_cache();
echo wp_json_encode( array( 'attachment' => $aid, 'url' => wp_get_attachment_url( $aid ), 'inserted' => ! $state['exists'], 'css' => sha1_file( get_stylesheet_directory() . '/' . $rel ) ) );
