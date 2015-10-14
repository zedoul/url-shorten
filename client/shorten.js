(function() {
  var Searcher = function(prefs) {
    var self = this;
    EventEmitter2.call(self);

    this.prefs = prefs;

    this.search = function(cb) {
      $.ajax({
        url: "http://0.0.0.0:5000/_ah/search",
        type: "get",
        async: true,
        dataType: "json",
        data: { 
               'link': prefs.link, 
              },
        success: function(response) {
          console.log(response)
          cb(null, response.url);
        }, 
        error: function(jqXHR, textStatus, errorThrown){
          console.log(arguments);
        }
      });
    };
  };

  var SearchControls = function(prefs) {
    var self = this;
    EventEmitter2.call(self);

    var $search = $('#controls .search');

    var $link = $('#controls .link').selectize({
      delimiter: '\n',
      persist: false,
      create: function(input) {
        return {value: input, text: input};
      }
    });

    $search.on('click', function() {
      self.emit('search');
      return false;
    });

    $link.on('change', function(e) {
      var val = $(e.target).val();
      self.emit('change:link', val); 
    });
  };

  var init = function() {
    var prefs = {
      link: []
    };

    var controls = new SearchControls(prefs);
    var searcher = new Searcher(prefs);

    controls.on('search', function() {
      searcher.search(function(err, shorten_url) {
        if (err) return alert(err);
        console.log(shorten_url);
      });
    });

    controls.on('change:link', function(link) {
      searcher.prefs.link = link;
    });
  };

  // Inherit from `EventEmitter2`.
  Searcher.prototype = Object.create(EventEmitter2.prototype);
  SearchControls.prototype = Object.create(EventEmitter2.prototype);

  // Boot the application.
  init();
}());
