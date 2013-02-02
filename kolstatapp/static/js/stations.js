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

			$.ajax({
				url: '/kolstat/ajax/favourites',
				dataType: 'jsonp'
			}).done(function(data){
				$.each(data, function(key, value){
					var btn = $('<img>').attr('src', '/static/img/picto/' + key + '.png').height($this.height()).addClass('picto');
					var $value = value;
					btn.click(function(){
						$this.val($value);
					});
					div.append(btn);
				});
			});

		});	
	};

	$(document).ready(function(){
		$('.stationField').stationField();
	});
})(jQuery);
