function themeconfig(themefolder, themename) {
  // Auxilary function to generate the task configuration for a single theme.
  var cfg = {
    options: {
      paths: [
        themefolder + '/static/css/' + themename, // theme folder
        'data_admin/common/static/css', // data admin folder
        'node_modules/bootstrap/less' // bootstrap folder
        ],
      strictMath: true,
      compress: true,
      relativeUrls: true,
      plugins: [
        new(require('less-plugin-autoprefix'))({
          browsers: ["last 2 versions"]
        })
      ]
    },
    files: {}
  }
  cfg.files[themefolder + '/static/css/' + themename + '/bootstrap.min.css'] = [
    'data_admin/common/static/css/frepple.less', // Generic frePPLe styles
    themefolder + '/static/css/' + themename + '/frepple.less' // Theme specific styles
    ]
  return cfg;
}

// Grunt configuration
module.exports = function (grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    // Less compilation
    less: {
      odoo: themeconfig('data_admin/common', 'odoo'),
      grass: themeconfig('data_admin/common', 'grass'),
      earth: themeconfig('data_admin/common', 'earth'),
      lemon: themeconfig('data_admin/common', 'lemon'),
      snow: themeconfig('data_admin/common', 'snow'),
      strawberry: themeconfig('data_admin/common', 'strawberry'),
      water: themeconfig('data_admin/common', 'water'),
      orange: themeconfig('data_admin/common', 'orange'),
      openbravo: themeconfig('data_admin/common', 'openbravo'),
    },
    // When any .less file changes we automatically run the "less"-task.
    watch: {
      files: ["**/*.less"],
      tasks: ["less"]
    },

    // Concatenate javascript files
    concat: {
      common: {
        src: [
              'data_admin/common/static/common/src/module.js',
              'data_admin/common/static/common/src/webfactory.js',
              'data_admin/common/static/common/src/preferences.js'
              ],
        dest: 'data_admin/common/static/js/frepple-common.js'
      },
    },

    // Uglify the javascript files
    uglify: {
      options: {
        sourceMap: true,
      },
      js: {
        src: ['data_admin/common/static/js/frepple.js'],
        dest: 'data_admin/common/static/js/frepple.min.js'
      },
      common: {
        src: ['data_admin/common/static/js/frepple-common.js'],
        dest: 'data_admin/common/static/js/frepple-common.min.js'
      },
    },

    // Clean intermediate files
    clean: [
      'data_admin/common/static/js/frepple-common.js'
      ]
  });

  // Load tasks
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-angular-gettext');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify-es');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-exec');

  // Register our tasks
  grunt.registerTask('minify', ['concat', 'uglify', 'clean']);
  grunt.registerTask('default', ['less', 'concat', 'uglify', 'clean']);

};
