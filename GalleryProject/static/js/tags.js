const tagDiv = document.getElementById('tags');
const tagInput = document.getElementById('id_tagCreate');
const tagForm = document.getElementById('id_tag');
tagInput.addEventListener('keydown', function (event) {
	if (event.key == 'Enter') {
		event.preventDefault();
		const tagCol = document.createElement('div');
		tagCol.className = 'col-3'
		const tag = document.createElement('p');
		tagCol.className = 'section-item'
		const tagText = tagInput.value.trim();

		if (tagText !== '') {
			tag.innerHTML = tagText;
			tag.value = tagText;
			tag.innerHTML += ' <a><i class="delete-button fa-solid fa-circle-xmark fa-2xs"></i></a>';
			tagForm.innerHTML += `<option selected value="${tagText}">${tagText}</option>`
			tagDiv.appendChild(tagCol);
			tagCol.appendChild(tag);
			tagInput.value = '';
		}
	}

});

tagDiv.addEventListener('click', function(event){
	if (event.target.classList.contains('delete-button')){
		const l1 = event.target.parentNode
		const l2 = l1.parentNode;
		const l3 = l2.parentNode;
		
		const tagVal = l2.value;
		getText(l2.value)
		console.log(tagVal)
		l1.remove();
		l2.remove();
		l3.remove();
	}
});

function getText(xTagval) {

	for (let i = 0; i < tagForm.length; i++) {
		let option = tagForm.options[i];
		if (option.value == xTagval) {
			option.remove();
		}
	}
}