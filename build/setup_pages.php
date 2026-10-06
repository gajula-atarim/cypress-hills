// Cypress Hills — deploy the brand-kit inner pages (run via Atarim execute-php).
// Fetches everything from one pinned commit of the repo and saves it through
// Elementor's document API. Re-running updates the same pages in place (matched by slug).
$ref  = '__REF__';
$gh   = 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/' . $ref . '/';
$get  = function ( $path ) use ( $gh ) {
	$r = wp_remote_get( $gh . $path, array( 'timeout' => 30 ) );
	if ( is_wp_error( $r ) || 200 !== wp_remote_retrieve_response_code( $r ) ) {
		throw new Exception( 'fetch failed: ' . $path );
	}
	return wp_remote_retrieve_body( $r );
};
$json = function ( $path ) use ( $get ) {
	$d = json_decode( $get( $path ), true );
	if ( ! is_array( $d ) ) {
		throw new Exception( 'bad json: ' . $path );
	}
	return $d;
};
$docs = \Elementor\Plugin::$instance->documents;
$save = function ( $id, $elements, $settings = array() ) use ( $docs ) {
	$docs->get( $id, false )->save( array( 'elements' => $elements, 'settings' => $settings ) );
	update_post_meta( $id, '_elementor_edit_mode', 'builder' );
};
$find = function ( $type, $title ) {
	$p = get_posts( array( 'post_type' => $type, 'title' => $title, 'post_status' => 'any', 'numberposts' => 1 ) );
	return $p ? $p[0]->ID : 0;
};
$out = array();

// 1. Child theme CSS + JS.
$dir = get_stylesheet_directory();
foreach ( array( 'assets/css/cypress-hills.css', 'assets/js/cypress-hills.js' ) as $rel ) {
	file_put_contents( $dir . '/' . $rel, $get( 'wp-content/themes/hello-elementor-child/' . $rel ) );
	$out['theme'][ $rel ] = sha1_file( $dir . '/' . $rel );
}

// 2. Contact page form (MetForm).
$cform = $find( 'metform-form', 'Contact Page Form' );
if ( ! $cform ) {
	$cform = \MetForm\Core\Forms\Builder::instance()->create_form( 'Contact Page Form', 0, array() );
}
$fs = get_post_meta( $cform, 'metform_form__form_setting', true );
$fs = is_array( $fs ) ? $fs : array();
$fs['success_message'] = 'Thanks, we’ve got it. Our office will call to book your site visit.';
$fs['store_entries']   = '1';
$fs['form_title']      = 'Contact Page Form';
update_post_meta( $cform, 'metform_form__form_setting', $fs );
$save( $cform, $json( 'build/out/contact-form.json' ) );
$out['contact_form'] = $cform;

// 3. Pages (Elementor Full Width template keeps the UAE header/footer).
$ids = array();
foreach ( $json( 'build/out/pages/index.json' ) as $pg ) {
	$existing = get_page_by_path( $pg['slug'], OBJECT, 'page' );
	$id       = $existing ? $existing->ID : wp_insert_post( array(
		'post_type'   => 'page',
		'post_title'  => $pg['title'],
		'post_name'   => $pg['slug'],
		'post_status' => 'publish',
	) );
	if ( is_wp_error( $id ) || ! $id ) {
		throw new Exception( 'page create failed: ' . $pg['slug'] );
	}
	wp_update_post( array( 'ID' => $id, 'post_title' => $pg['title'], 'post_status' => 'publish' ) );
	update_post_meta( $id, '_wp_page_template', 'elementor_header_footer' );
	$tree = wp_json_encode( $json( 'build/out/pages/' . $pg['slug'] . '.json' ) );
	$tree = str_replace( '"mf_form_id":"CONTACT_FORM_ID"', '"mf_form_id":"' . $cform . '"', $tree );
	$save( $id, json_decode( $tree, true ), array( 'template' => 'elementor_header_footer', 'hide_title' => 'yes' ) );
	$ids[ $pg['slug'] ] = $id;
}
$out['pages'] = $ids;

// 4. Header, footer and home page (links now point at the real pages).
$hdr  = $find( 'elementor-hf', 'Site Header' );
$ftr  = $find( 'elementor-hf', 'Site Footer' );
$home = (int) get_option( 'page_on_front' );
$form = $find( 'metform-form', 'Home Contact Form' );
$save( $hdr, $json( 'build/out/header.json' ) );
$save( $ftr, $json( 'build/out/footer.json' ) );
$tree = str_replace( '"mf_form_id":"0"', '"mf_form_id":"' . $form . '"', wp_json_encode( $json( 'build/out/home.json' ) ) );
$save( $home, json_decode( $tree, true ), array( 'template' => 'elementor_header_footer', 'hide_title' => 'yes' ) );

// 5. Primary menu built from the pages, so WordPress marks the current page/section.
$menu = wp_get_nav_menu_object( 'Primary Menu' );
foreach ( (array) wp_get_nav_menu_items( $menu->term_id ) as $it ) {
	wp_delete_post( $it->ID, true );
}
$add = function ( $page_id, $parent = 0, $label = '' ) use ( $menu ) {
	return wp_update_nav_menu_item( $menu->term_id, 0, array(
		'menu-item-object-id' => $page_id,
		'menu-item-object'    => 'page',
		'menu-item-type'      => 'post_type',
		'menu-item-status'    => 'publish',
		'menu-item-parent-id' => $parent,
		'menu-item-title'     => $label,
	) );
};
$add( $home, 0, 'Home' );
$add( $ids['about'] );
$s = $add( $ids['services'] );
foreach ( array( 'backyard-putting-greens', 'golf-course-shaping', 'armor-stone-walls', 'artificial-grass-installation', 'synthetic-turf-installation' ) as $slug ) {
	$add( $ids[ $slug ], $s );
}
$p = $add( $ids['pools'] );
$add( $ids['fiberglass-pool-installation'], $p );
$add( $ids['swimming-pool-installation-caledon'], $p, 'Swimming Pool Installation Caledon ON' );
$add( $ids['projects'] );
$out['menu'] = count( wp_get_nav_menu_items( $menu->term_id ) );

// Pretty permalinks so /services/ etc. resolve.
if ( '' === get_option( 'permalink_structure' ) ) {
	update_option( 'permalink_structure', '/%postname%/' );
}
flush_rewrite_rules( false );
\Elementor\Plugin::$instance->files_manager->clear_cache();
echo wp_json_encode( $out );
