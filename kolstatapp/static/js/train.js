function addCar(id){
	wagon = $('<img src="/static/img/carriages/' + id + '.png" />').attr('alt', id);
	wagon.dblclick(function(){ $(this).remove(); update_form();});
	$('.composition .carriages').append(wagon);
	update_form();
}

carriages = {
	lok: ['EP07', 'EP09', 'ET22', 'EU07', 'EP08', 'SM42'],
	car1: ['Admnu', 'Adnu'],
	car2: ['Bdhpumn', 'Bdmnu', 'Bdnu', 'Bc', 'BDdsu'],
	ezt: ['EN57', 'ED72', 'ED74', 'EN75', 'EN94', 'EN95'],
	szt: ['SA110', 'SA131', 'SA134'],
	other: ['ABdnu', 'WLAB', 'WRbd']
};

desc = {
	lok: 'lokomotywy',
	car1: 'wagony klasy 1',
	car2: 'wagony klasy 2',
	ezt: 'elektryczne zespoły trakcyjne',
	szt: 'spalinowe zespoły trakcyjne',
	other: 'inne'
};

function get_composition_from_element(elem){
	var result = '';
	elem.each(function(){
		if(result != '' ) result += '+';
		result += $(this).attr('alt');
	});
	return result;
}

function get_user_composition(){
	return get_composition_from_element($('.composition .carriages').children('img'));
}

function get_composition(){
	elem = $('.compselect.selected');
	if(elem.hasClass('manual')) return get_user_composition();
	td = elem.parent().prev().children();
	return get_composition_from_element(td);
}

function update_form(){
	$('input[name=composition]').val(get_composition());
}

function prepare_composition(){
	$('.composition').append('<div class="carriages"/>');
	add_new = $('<div class="add_new"/>').hide();
	
	hs_button = $('<button />').text('Pokaż/ukryj wagony').button().click(function(){ add_new.slideToggle(); });
	manual = $('<button />').text('Wybierz własne').button().addClass('compselect').addClass('manual');
	
	$('.composition').append(hs_button).append(manual).append(add_new);
	
	$('.composition .carriages').sortable({
		update: update_form
	});

	table = $('<table>');
	tr1 = $('<tr />');
	for(k in carriages){tr1.append($('<td/>').text(desc[k]));}
	tr2 = $('<tr />');
	for(k in carriages){
		tdx = $('<td />');
		for(l in carriages[k]){
			tdx.append($('<img />', {'class': 'addable', id: carriages[k][l], src: '/static/img/carriages/' + carriages[k][l] + '.png', alt: carriages[k][l]}));
			tdx.append($('<p />').append($('<a/>').text(carriages[k][l]).attr('href', '/kolstat/carriages/' + carriages[k][l] + '/')));
		} 
		tr2.append(tdx);
	}
	
	table.append(tr1);
	table.append(tr2);

	$('.composition .add_new').append(table);

	$('.add_new img.addable').click(function(){
		addCar(this.id);
	});


}

$(document).ready(prepare_composition);
