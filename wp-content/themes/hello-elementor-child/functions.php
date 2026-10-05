<?php
/**
 * Cypress Hills (Hello Elementor Child) functions.
 *
 * @package hello-elementor-child
 */

defined( 'ABSPATH' ) || exit;

define( 'CH_CHILD_VERSION', '1.0.0' );

add_action( 'wp_enqueue_scripts', function () {
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css' );

	// Archivo is a variable font with a width axis; the design uses font-stretch 112–118%,
	// so it is loaded from the CSS2 API (Elementor's own Google Fonts loader omits the axis).
	wp_enqueue_style(
		'ch-fonts',
		'https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap',
		array(),
		null
	);

	wp_enqueue_style(
		'ch-site',
		$uri . '/assets/css/cypress-hills.css',
		array( 'parent-style', 'ch-fonts' ),
		file_exists( $dir . '/assets/css/cypress-hills.css' ) ? filemtime( $dir . '/assets/css/cypress-hills.css' ) : CH_CHILD_VERSION
	);

	wp_enqueue_script(
		'ch-site',
		$uri . '/assets/js/cypress-hills.js',
		array(),
		file_exists( $dir . '/assets/js/cypress-hills.js' ) ? filemtime( $dir . '/assets/js/cypress-hills.js' ) : CH_CHILD_VERSION,
		true
	);
}, 20 );

add_action( 'wp_head', function () {
	echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
}, 1 );
