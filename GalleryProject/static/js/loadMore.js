

const loaderRow = document.getElementById('loaderRow');
let nextPage = 1;
const url = document.getElementById('loadMore').value;
console.log(url)
const loadBtn = document.getElementById('loadMore');
const loaderBar = document.getElementById('dotsLoader');
const subgal = document.getElementById('subgal').value;
const lastPage = document.getElementById('lastPage').value;
const pageName = document.getElementById('pageName').value;
console.log(subgal, lastPage)

document.getElementById("loadMore").addEventListener("click", function(event){
	event.preventDefault();
	nextPage ++;
	const data = {'next_p': nextPage, 'keyler': 'loadMore'}
	
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

		})
		.then(res => res.json())
		.then(responseData => {
			console.log(nextPage, lastPage)
			if (nextPage == lastPage){
				loaderBar.style.display = 'none';
			} else {
				loaderBar.style.display = 'none';
				loadBtn.style.display = 'inline-block';
			};
			if (pageName == 'gal'){
				galleryDivs(responseData);
			};

	}).catch(error => console.error('Error:', error));
});

function galleryDivs(gallerryData){
	for(let data_set of gallerryData){

		let itemDisplay =data_set.display;
		let itemId = data_set.id;
		let itemTitle = data_set.title;
		let itemImage = data_set.image_link;
		let itemProject = data_set.project;

		// creates the container to hold the images list data
		const parentCol = document.createElement('div');
		parentCol.className = 'col mt-4 mb-4 slide-up';
		parentCol.id = 'slide-in'
		loaderRow.appendChild(parentCol);

		// creates the image card
		const imageCardDi = document.createElement('div');
		if (itemDisplay == subgal){
			imageCardDi.className = 'image-card-a';
		} else {
			imageCardDi.className = 'image-card';
		}
		parentCol.appendChild(imageCardDi);

		const itemCheckDiv = document.createElement('input');
		itemCheckDiv.className = 'noshow checkImage form-check-input';
		itemCheckDiv.type = "checkbox";
		itemCheckDiv.name = 'checkbox' + itemId;
		itemCheckDiv.value=itemId; 
		itemCheckDiv.id = "id_check" + itemId;
		imageCardDi.appendChild(itemCheckDiv);

		// creates the image card info
		const imageInfoDi = document.createElement('label');
		imageInfoDi.className = 'image-card-info';
		imageInfoDi.htmlFor = "id_check" + itemId;
		imageCardDi.appendChild(imageInfoDi);

		const itemImageDiv = document.createElement('img');
		itemImageDiv.src = itemImage;
		itemImageDiv.load = 'lazy';
		itemImageDiv.className = 'image-list';
		imageInfoDi.appendChild(itemImageDiv);

		//creates the row for the item data columns 
		const itemRow = document.createElement('div');
		itemRow.className = 'row title';
		imageInfoDi.appendChild(itemRow);

		// id field 
		const itemField2 = document.createElement('div');
		itemField2.className = 'col-6';
		itemRow.appendChild(itemField2);	

		const itemIdDiv = document.createElement('p');
		itemIdDiv.className = 'p-p';
		itemIdDiv.innerHTML = 'ID: #' +itemId ;
		itemField2.appendChild(itemIdDiv);

		// project name field
		const itemField3 = document.createElement('div');
		itemField3.className = 'col-12';
		itemRow.appendChild(itemField3);

		const itemProjectDiv = document.createElement('p');
		itemProjectDiv.className = 'p-p';
		itemProjectDiv.innerHTML = 'Project: '+ itemProject;
		itemField3.appendChild(itemProjectDiv);

		// image titel
		const itemField4 = document.createElement('div');
		itemField4.className = 'col-12';
		itemRow.appendChild(itemField4);

		const itemtitleDiv = document.createElement('p');
		itemtitleDiv.className = 'p-p';
		itemtitleDiv.innerHTML ='Title: ' + itemTitle;
		itemField4.appendChild(itemtitleDiv);
	};
}

