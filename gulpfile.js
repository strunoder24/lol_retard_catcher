const { series, watch } = require('gulp');
const gulp = require('gulp');
const sass = require('gulp-sass');
const rename = require('gulp-rename');
const uglify = require('gulp-uglify');
const concat = require('gulp-concat');
const cleanCSS = require('gulp-clean-css');

//move external libs to static
function move_externals_js() {
    return gulp.src('frontend/external_libs/*.js')
        .pipe(uglify())
        .pipe(gulp.dest('static/js'))
}


function move_externals_css() {
    return gulp.src('frontend/external_libs/*.css')
        .pipe(cleanCSS())
        .pipe(gulp.dest('static/css'))
}


//compile sass into css
function style() {
    return gulp.src('frontend/styles/index.sass')
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(rename('styles.css'))
        .pipe(gulp.dest('static/css'))
}

function scripts() {
    return gulp.src('frontend/js/*.js')
        .pipe(concat('main.js'))
        // .pipe(uglify())
        .pipe(gulp.dest('static/js'))
}


exports.collectExternals = series(move_externals_js, move_externals_css);
exports.default = function () {
    watch('frontend/styles/**/*.sass', {ignoreInitial: false}, style);
    watch('frontend/js/*.js', {ignoreInitial: false}, scripts);
};