// Cypress Hills — re-save only the Home page from a pinned commit (run via Atarim execute-php),
// then re-apply presentation mode (build/present_mode.php) so other-page links stay "#".
$ref = '__REF__';
$gh  = 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/' . $ref . '/';
$get = function ( $path ) use ( $gh ) {
	$r = wp_remote_get( $gh . $path, array( 'timeout' => 30 ) );
	if ( is_wp_error( $r ) || 200 !== wp_remote_retrieve_response_code( $r ) ) {
		throw new Exception( 'fetch failed: ' . $path );
	}
	return wp_remote_retrieve_body( $r );
};
$form = get_posts( array( 'post_type' => 'metform-form', 'title' => 'Home Contact Form', 'post_status' => 'any', 'numberposts' => 1 ) );
// Re-encode first: the repo file is pretty-printed ("key": "value"), the placeholder match needs compact JSON.
$tree = wp_json_encode( json_decode( $get( 'build/out/home.json' ), true ) );
if ( false === strpos( $tree, '"mf_form_id":"0"' ) ) {
	throw new Exception( 'form placeholder not found' );
}
$tree = str_replace( '"mf_form_id":"0"', '"mf_form_id":"' . $form[0]->ID . '"', $tree );
$data = json_decode( $tree, true );
if ( ! is_array( $data ) ) {
	throw new Exception( 'bad home.json' );
}
$home = (int) get_option( 'page_on_front' );
\Elementor\Plugin::$instance->documents->get( $home, false )->save( array( 'elements' => $data, 'settings' => array( 'template' => 'elementor_header_footer', 'hide_title' => 'yes' ) ) );
echo 'home saved | ';
eval( $get( 'build/present_mode.php' ) );
