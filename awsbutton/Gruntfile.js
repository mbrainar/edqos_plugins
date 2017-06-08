module.exports = function(grunt) {

  grunt.initConfig({
    lambda_invoke: {
      default: {
        options: {

        }
      }
    },
  });

  grunt.loadNpmTasks('grunt-aws-lambda');

  grunt.registerTask('default', ['lambda_invoke']);

};
