var _fav_cache = [];

function build_cache(next){
	if(_fav_cache.length) return ;
	jQuery.ajax({
		url: '/kolstat/ajax/favourites/',
		dataType: 'jsonp'
	}).done(function(data){
		_fav_cache = data;
		next.stationField();
	});
}

(function( $ ){
	$.fn.stationField = function (){
		return this.each(function(){
			var $this = $(this);

			var div = $('<span>');
			$this.replaceWith(div);
			div.append($this);

			$this.autocomplete({
				source: function(request, response){
					$.ajax({
						url: "/kolstat/ajax/station/",
						dataType: 'jsonp',
						data: {
							query: request.term,
							type: 'name'
						}
					}).done(function(data){
						response( data );
					});
				},
				minLength: 3
			}).change(function(){
				var $input = $(this);
				var value = $(this).val();
				if(! /^[0-9]+/.test(value)) return true;
				$.ajax({
					url: "/kolstat/ajax/station/",
					dataType: 'jsonp',
					data: {
						query: value,
						type: 'kurs90'
					}
				}).done(function(data){
					if(data.length == 1) 
						$input.val(data[0]);
				});
					
			});
		
			$.each(_fav_cache, function(key, value){
				var btn = $('<img>').attr('src', '/static/img/picto/' + key + '.png').height($this.height()).addClass('picto');
				var $value = value;
				btn.click(function(){
					$this.val($value);
				});
				div.append(btn);
			});
		});	
	};

	$(document).ready(function(){
		fields = $('.stationField');
		if(fields){
			build_cache(fields);
		} else {
			fields.stationField();
		}
	});
})(jQuery);
