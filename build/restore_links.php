// Cypress Hills — end presentation mode (run via Atarim execute-php): put the real page links back.
// Re-saves only the Site Header, Site Footer and Home page from a pinned commit, and rebuilds the
// Primary Menu from the pages. The other pages are not touched.
$ref = '__REF__';
$gh  = 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/' . $ref . '/';
$json = function ( $path ) use ( $gh ) {
	$r = wp_remote_get( $gh . $path, array( 'timeout' => 30 ) );
	if ( is_wp_error( $r ) || 200 !== wp_remote_retrieve_response_code( $r ) ) {
		throw new Exception( 'fetch failed: ' . $path );
	}
	$d = json_decode( wp_remote_retrieve_body( $r ), true );
	if ( ! is_array( $d ) ) {
		throw new Exception( 'bad json: ' . $path );
	}
	return $d;
};
$find = function ( $type, $title ) {
	$p = get_posts( array( 'post_type' => $type, 'title' => $title, 'post_status' => 'any', 'numberposts' => 1 ) );
	return $p ? $p[0]->ID : 0;
};
$page = function ( $slug ) {
	$p = get_page_by_path( $slug, OBJECT, 'page' );
	if ( ! $p ) {
		throw new Exception( 'missing page: ' . $slug );
	}
	return $p->ID;
};
$docs = \Elementor\Plugin::$instance->documents;
$home = (int) get_option( 'page_on_front' );
$form = $find( 'metform-form', 'Home Contact Form' );
$tree = wp_json_encode( $json( 'build/out/home.json' ) );
if ( false === strpos( $tree, '"mf_form_id":"0"' ) ) {
	throw new Exception( 'form placeholder not found' );
}
$tree = str_replace( '"mf_form_id":"0"', '"mf_form_id":"' . $form . '"', $tree );
$docs->get( $find( 'elementor-hf', 'Site Header' ), false )->save( array( 'elements' => $json( 'build/out/header.json' ) ) );
$docs->get( $find( 'elementor-hf', 'Site Footer' ), false )->save( array( 'elements' => $json( 'build/out/footer.json' ) ) );
$docs->get( $home, false )->save( array( 'elements' => json_decode( $tree, true ), 'settings' => array( 'template' => 'elementor_header_footer', 'hide_title' => 'yes' ) ) );

$menu = wp_get_nav_menu_object( 'Primary Menu' );
foreach ( (array) wp_get_nav_menu_items( $menu->term_id ) as $it ) {
	wp_delete_post( $it->ID, true );
}
$add = function ( $page_id, $parent = 0, $label = '', $classes = '' ) use ( $menu ) {
	return wp_update_nav_menu_item( $menu->term_id, 0, array(
		'menu-item-object-id' => $page_id,
		'menu-item-object'    => 'page',
		'menu-item-type'      => 'post_type',
		'menu-item-status'    => 'publish',
		'menu-item-parent-id' => $parent,
		'menu-item-title'     => $label,
		'menu-item-classes'   => $classes,
	) );
};
$add( $home, 0, 'Home' );
$add( $page( 'about' ) );
$s = $add( $page( 'services' ) );
foreach ( array( 'backyard-putting-greens', 'golf-course-shaping', 'armor-stone-walls', 'artificial-grass-installation', 'synthetic-turf-installation' ) as $slug ) {
	$add( $page( $slug ), $s );
}
$p = $add( $page( 'pools' ) );
$add( $page( 'fiberglass-pool-installation' ), $p );
$add( $page( 'swimming-pool-installation-caledon' ), $p, 'Swimming Pool Installation Caledon ON' );
$add( $page( 'projects' ) );
$add( $page( 'contact' ), 0, 'Contact Us', 'ch-menu-cta' );
\Elementor\Plugin::$instance->files_manager->clear_cache();
$hash = 0;
foreach ( array( $home ) as $id ) {
	$hash += substr_count( wp_json_encode( $docs->get( $id, false )->get_elements_data() ), '"url":"#"' );
}
echo wp_json_encode( array( 'menu_items' => count( wp_get_nav_menu_items( $menu->term_id ) ), 'home_hash_links_left' => $hash ) );
