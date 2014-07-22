'use strict';

angular.module("galaxymodule", ["tutorialApp", "ngViewExample", "mydropdownapp"]);

// module for first inocent experiments with angular //
angular.module('tutorialApp', ['ngAnimate'])
  .directive('price', function(){
  return {
    restrict: 'E',
    scope: {
      value: '='
    },
    template: '<span ng-show="value == 0">kostenlos</span>' +
      '<span ng-show="value > 0">{{value | currency}}</span>'
  }
  })
  .factory('Cart', function() {
    var items = [];
    return {
      getItems: function() {
        return items;
      },
      addArticle: function(article) {
        items.push(article);
      },
      sum: function() {
        return items.reduce(function(total, article) {
          return total + article.price;
        }, 0);
      }
    };
  })
  .controller('ArticlesCtrl', function($scope, $http, Cart){
    $scope.cart = Cart;
    $http.get('/static/arkiwimain/json/articles.json').then(function(articlesResponse) {
      $scope.articles = articlesResponse.data;
    });
  })
  .controller('CartCtrl', function($scope, Cart){
    $scope.cart = Cart;
  });

// module from https://docs.angularjs.org/api/ngRoute/directive/ngView
angular.module('ngViewExample', ['ngRoute', 'ngAnimate'])
  .config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) {
      $routeProvider
        .when('/Book/:bookId', {
          templateUrl: 'book.html',
          controller: 'BookCtrl',
          controllerAs: 'book'
        })
        .when('/Book/:bookId/ch/:chapterId', {
          templateUrl: 'chapter.html',
          controller: 'ChapterCtrl',
          controllerAs: 'chapter'
        });

      // configure html5 to get links working on jsfiddle
      $locationProvider.html5Mode(true);
  }])
  .controller('MainCtrl', ['$route', '$routeParams', '$location',
    function($route, $routeParams, $location) {
      this.$route = $route;
      this.$location = $location;
      this.$routeParams = $routeParams;
  }])
  .controller('BookCtrl', ['$routeParams', function($routeParams) {
    this.name = "BookCtrl";
    this.params = $routeParams;
  }])
  .controller('ChapterCtrl', ['$routeParams', function($routeParams) {
    this.name = "ChapterCtrl";
    this.params = $routeParams;
  }]);

// module for dropdown
angular.module('mydropdownapp', ['ui.bootstrap'])
  .factory("menuService", ["$rootScope", function($rootScope) {        
        return { 
            menu: function() {
                $rootScope.globalMenu;
            },    
            setMenu: function(menu) {
                $rootScope.globalMenu = menu;
            }
        };
   
    }])
  .controller("MainController", ["$scope", "menuService", 
        function($scope, menuService){

            menuService.setMenu([{href:"#", label:"Dropdown",
                                    dropdown:[{href:"/edit", label:"Edit"}]},
                                 {href:'/', label:'test'}]);
                                 
            $scope.bodyText = "Some text";
            


        }]);