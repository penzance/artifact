(function()
{

  var app = angular.module('app', ['ngSanitize', 'ngAnimate', 'ng.django.urls'])
    .config(function($httpProvider)
    {
      $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      $httpProvider.interceptors.push(function()
      {
        return {
          'request': function(config)
          {
            // window.globals.append_resource_link_id function added by
            // django_auth_lti/js/resource_link_id.js
            config.url = window.globals.append_resource_link_id(config.url);
            return config;
          }
        };
      });
    });
})();