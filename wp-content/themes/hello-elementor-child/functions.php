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

	// Brand fonts (brand kit Typography Spec): Source Serif 4 for headings, Roboto for UI/body.
	wp_enqueue_style(
		'ch-fonts',
		'https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap',
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
