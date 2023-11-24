const imageRow = document.getElementById('imageRow');
let nextPage = 1;
const url = document.getElementById('loadMore').value;
console.log(url)
const loadBtn = document.getElementById('loadMore');
const loaderBar = document.getElementById('dotsLoader');
const subgal = document.getElementById('subgal').value;
const lastPage = document.getElementById('lastPage').value;
console.log(subgal, lastPage)

document.getElementById("loadMore").addEventListener("click", function(event){
	event.preventDefault();
	nextPage ++;
	const data = {'next_p': nextPage, 'keyler': 'loadMore'}
	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	const csrftoken = getCookie('csrftoken');
	loadBtn.style.display = 'none'
	loaderBar.style.display = 'flex'

	fetch(url, {
		method: 'POST', 
		body: JSON.stringify(data), 
		credentials: 'same-origin',

		headers: {
			'keyler': 'loadMore',
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		}

		}).then(res => res.json())
		.then(responseData => {
			if (nextPage == lastPage){
				loaderBar.style.display = 'none';
			} else {
				loaderBar.style.display = 'none';
				loadBtn.style.display = 'inline-block';
			};

			for(let data_set of responseData){

				let itemDisplay =data_set.display;
				let itemId = data_set.id;
				let itemTitle = data_set.title;
				let itemImage = data_set.image_link;
				let itemProject = data_set.project;

				// creates the container to hold the images list data
				parentCol = document.createElement('div');
				parentCol.className = 'col-12 mb-4';
				imageRow.appendChild(parentCol);

				//creates the row for the item data columns 
				itemRow = document.createElement('div');
				itemRow.className = 'row';
				parentCol.appendChild(itemRow);

				// check box field
				itemFeild1 = document.createElement('div');
				itemFeild1.className = 'col-6 col-md-3'
				itemRow.appendChild(itemFeild1);
				
				itemCheckLabel = document.createElement('p');
				itemCheckLabel.className = 'p-p'
				itemCheckLabel.innerHTML = 'Include'
				itemFeild1.appendChild(itemCheckLabel)

				brDiv = document.createElement('br')
				itemCheckLabel.appendChild(brDiv)

				itemCheckDiv = document.createElement('input');
				itemCheckDiv.className = 'form-check-input text-center'
				itemCheckDiv.type = "checkbox" 
				itemCheckDiv.name = 'checkbox' + itemId  
				itemCheckDiv.value=itemId 
				itemCheckDiv.id = "id_check"
				console.log(itemDisplay, subgal)
				if (itemDisplay == subgal){
					itemCheckDiv.checked = true
				};
				itemCheckLabel.appendChild(itemCheckDiv)

				// id field 
				itemFeild2 = document.createElement('div');
				itemFeild2.className = 'col-12 col-md-1'
				itemRow.appendChild(itemFeild2);

				itemIdDiv = document.createElement('p');
				itemIdDiv.className = 'p-p';
				itemIdDiv.innerHTML = '#' + itemId
				itemFeild2.appendChild(itemIdDiv)

				// project name field
				itemFeild3 = document.createElement('div');
				itemFeild3.className = 'col-12 col-md-4'
				itemRow.appendChild(itemFeild3);

				itemProjectDiv = document.createElement('p');
				itemProjectDiv.className = 'p-p';
				itemProjectDiv.innerHTML = itemProject
				itemFeild3.appendChild(itemProjectDiv)

				// image titel
				itemFeild4 = document.createElement('div');
				itemFeild4.className = 'col-12 col-md-4'
				itemRow.appendChild(itemFeild4);

				itemtitleDiv = document.createElement('p');
				itemtitleDiv.className = 'p-p';
				itemtitleDiv.innerHTML = itemTitle
				itemFeild4.appendChild(itemtitleDiv)

				// image field
				itemFeild5 = document.createElement('div');
				itemFeild5.className = 'col-12 text-center col-md-12'
				itemRow.appendChild(itemFeild5);

				itemImageDiv = document.createElement('img');
				itemImageDiv.src = itemImage
				itemImageDiv.load = 'lazy'
				itemImageDiv.className = 'image-list'
				itemFeild5.appendChild(itemImageDiv)

				hrDiv = document.createElement('hr')
				parentCol.appendChild(hrDiv)
			};

	}).catch(error => console.error('Error:', error));

	  	
});