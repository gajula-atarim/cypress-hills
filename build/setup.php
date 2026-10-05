// Cypress Hills — one-shot site setup, run via Atarim execute-php.
// Pulls the generated Elementor trees from the repo and saves them through
// Elementor's document API (so CSS, slashing and versions are handled by Elementor).
$base = 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/claude/sweet-meitner-vd48mz/build/out/';
$fetch = function ( $file ) use ( $base ) {
	$r = wp_remote_get( $base . $file . '?v=' . time(), array( 'timeout' => 30 ) );
	if ( is_wp_error( $r ) || 200 !== wp_remote_retrieve_response_code( $r ) ) {
		throw new Exception( 'fetch failed: ' . $file );
	}
	$data = json_decode( wp_remote_retrieve_body( $r ), true );
	if ( ! is_array( $data ) ) {
		throw new Exception( 'bad json: ' . $file );
	}
	return $data;
};
$find = function ( $type, $title ) {
	$p = get_posts( array( 'post_type' => $type, 'title' => $title, 'post_status' => 'any', 'numberposts' => 1 ) );
	return $p ? $p[0]->ID : 0;
};
$save = function ( $id, $elements, $settings = array() ) {
	$doc = \Elementor\Plugin::$instance->documents->get( $id, false );
	$doc->save( array( 'elements' => $elements, 'settings' => $settings ) );
	update_post_meta( $id, '_elementor_edit_mode', 'builder' );
};
$out = array();

// 0. Child theme files (functions.php, CSS, JS) from the repo.
$theme_dir = get_stylesheet_directory();
$theme_base = 'https://raw.githubusercontent.com/gajula-atarim/cypress-hills/claude/sweet-meitner-vd48mz/wp-content/themes/hello-elementor-child/';
foreach ( array( 'style.css', 'functions.php', 'assets/css/cypress-hills.css', 'assets/js/cypress-hills.js' ) as $rel ) {
	$r = wp_remote_get( $theme_base . $rel . '?v=' . time(), array( 'timeout' => 30 ) );
	if ( is_wp_error( $r ) || 200 !== wp_remote_retrieve_response_code( $r ) ) {
		throw new Exception( 'theme fetch failed: ' . $rel );
	}
	wp_mkdir_p( dirname( $theme_dir . '/' . $rel ) );
	file_put_contents( $theme_dir . '/' . $rel, wp_remote_retrieve_body( $r ) );
	$out['theme'][ $rel ] = sha1_file( $theme_dir . '/' . $rel );
}

// Elementor + theme options.
update_option( 'elementor_google_font', '0' );            // Archivo (with width axis) is loaded by the child theme.
update_option( 'elementor_disable_color_schemes', 'yes' );
update_option( 'elementor_disable_typography_schemes', 'yes' );
update_option( 'elementor_load_fa4_shim', '' );

// 1. MetForm contact form.
$form_id = $find( 'metform-form', 'Home Contact Form' );
if ( ! $form_id ) {
	$form_id = \MetForm\Core\Forms\Builder::instance()->create_form( 'Home Contact Form', 0, array() );
}
$fs = get_post_meta( $form_id, 'metform_form__form_setting', true );
$fs = is_array( $fs ) ? $fs : array();
$fs['success_message'] = 'Thanks, we’ve got it. Our office will be in touch shortly.';
$fs['store_entries']   = '1';
$fs['form_title']      = 'Home Contact Form';
update_post_meta( $form_id, 'metform_form__form_setting', $fs );
$save( $form_id, $fetch( 'form.json' ) );
$out['form'] = $form_id;

// 2. UAE header + footer templates.
foreach ( array( 'header' => array( 'Site Header', 'type_header' ), 'footer' => array( 'Site Footer', 'type_footer' ) ) as $key => $cfg ) {
	$id = $find( 'elementor-hf', $cfg[0] );
	if ( ! $id ) {
		$id = wp_insert_post( array( 'post_type' => 'elementor-hf', 'post_title' => $cfg[0], 'post_status' => 'publish' ) );
	}
	update_post_meta( $id, 'ehf_template_type', $cfg[1] );
	update_post_meta( $id, 'ehf_target_include_locations', array( 'rule' => array( 'basic-global' ), 'specific' => array() ) );
	update_post_meta( $id, 'ehf_target_exclude_locations', array() );
	update_post_meta( $id, 'ehf_target_user_roles', array( 'all' ) );
	update_post_meta( $id, '_wp_page_template', 'elementor_canvas' );
	$save( $id, $fetch( $key . '.json' ) );
	$out[ $key ] = $id;
}

// 3. Home page (Elementor Full Width keeps the UAE header/footer).
$home_id = $find( 'page', 'Home' );
if ( ! $home_id ) {
	$home_id = wp_insert_post( array( 'post_type' => 'page', 'post_title' => 'Home', 'post_name' => 'home', 'post_status' => 'publish' ) );
}
update_post_meta( $home_id, '_wp_page_template', 'elementor_header_footer' );
$tree = $fetch( 'home.json' );
$json = wp_json_encode( $tree );
$json = str_replace( '"mf_form_id":"0"', '"mf_form_id":"' . $form_id . '"', $json );
$save( $home_id, json_decode( $json, true ), array( 'template' => 'elementor_header_footer', 'hide_title' => 'yes' ) );
update_option( 'show_on_front', 'page' );
update_option( 'page_on_front', $home_id );
$out['home'] = $home_id;

// 4. Primary menu (UAE Navigation Menu reads this).
$menu = wp_get_nav_menu_object( 'Primary Menu' );
if ( $menu ) {
	foreach ( (array) wp_get_nav_menu_items( $menu->term_id ) as $it ) {
		wp_delete_post( $it->ID, true );
	}
	$add = function ( $label, $url, $parent = 0 ) use ( $menu ) {
		return wp_update_nav_menu_item( $menu->term_id, 0, array(
			'menu-item-title'     => $label,
			'menu-item-url'       => $url,
			'menu-item-type'      => 'custom',
			'menu-item-status'    => 'publish',
			'menu-item-parent-id' => $parent,
		) );
	};
	$add( 'Home', home_url( '/' ) );
	$s = $add( 'Services', home_url( '/#services' ) );
	foreach ( array( 'Backyard Putting Greens', 'Golf Course Shaping', 'Armor Stone Walls', 'Artificial Grass Installation', 'Synthetic Turf Installation' ) as $l ) {
		$add( $l, home_url( '/#services' ), $s );
	}
	$p = $add( 'Pools', home_url( '/#services' ) );
	foreach ( array( 'Fiberglass Pool Installation', 'Swimming Pool Installation Caledon ON' ) as $l ) {
		$add( $l, home_url( '/#services' ), $p );
	}
	$add( 'Projects', home_url( '/#work' ) );
	$out['menu'] = $menu->term_id;
}

\Elementor\Plugin::$instance->files_manager->clear_cache();
echo wp_json_encode( $out );
