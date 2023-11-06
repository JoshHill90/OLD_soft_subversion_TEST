let itemCounter = 0;
const numberDisplayed = document.getElementById('total');
var totalPaid = {};
let liveTotal = 0;

function newItem(){
	const parentDiv = document.getElementById('lineItems')

	itemCounter +=1;

	const itemCost = document.createElement('input');
	itemCost.className = 'form-control mt-2 mb-4';
	itemCost.name = 'line_item_cost' + itemCounter;
	itemCost.type = 'number';
	itemCost.placeholder = '0.00';
	itemCost.required = true
	itemCost.id = 'id_line_item_cost' + itemCounter;

	itemCost.addEventListener('input', function() {
		updateTotal(itemCost.id, itemCost.valueAsNumber);
	});
	


	const itemReceipt = document.createElement('input');
	itemReceipt.className = 'form-control mt-2 mb-4';
	itemReceipt.name = 'line_item_receipt' + itemCounter;
	itemReceipt.type = 'text';
	itemReceipt.required = true
	itemReceipt.id = 'id_line_item_receipt' + itemCounter;

	const cancelItem = document.createElement('button');
	cancelItem.className = 'fa-solid mt-4 mb-2 fa-xmark btn-icon';
	cancelItem.type = 'button';
	cancelItem.id = 'cancelItemBtn' + itemCounter;
	

	const nestDiv1 = document.createElement('div');
	const nestDiv2 = document.createElement('div');
	const nestDiv3 = document.createElement('div');
	const nesthr = document.createElement('hr');

	nestDiv1.id = 'itemDiv1C' + itemCounter; 
	nestDiv2.id = 'itemDiv2C' + itemCounter; 
	nestDiv3.id = 'itemDiv3C' + itemCounter;
	nesthr.id = 'hrDivC' + itemCounter;

	nestDiv1.className = 'col-5';
	nestDiv2.className = 'col-5';
	nestDiv3.className = 'col-2 text-center';
	nestDiv1.appendChild(itemCost);
	nestDiv2.appendChild(itemReceipt);
	nestDiv3.appendChild(cancelItem);
	parentDiv.appendChild(nestDiv1);
	parentDiv.appendChild(nestDiv2);
	parentDiv.appendChild(nestDiv3);
	parentDiv.appendChild(nesthr);

	cancelItem.addEventListener('click', function() {
		removeItem(nestDiv1.id, nestDiv2.id, nestDiv3.id, nesthr.id);
		deleteFromtotal(itemCost.id);
	});

};

function removeItem(itemID1, itemID2, itemID3, hrID) {
	const remover1 = document.getElementById(itemID1);
	const remover2 = document.getElementById(itemID2);
	const remover3 = document.getElementById(itemID3);
	const remover4 = document.getElementById(hrID);
	if(remover1){
		remover1.remove();
	};
	if(remover2){
		remover2.remove();
	};
	if(remover3){
		remover3.remove();
	};
	if(remover4){
		remover4.remove();
	};
};

function updateLiveTotal() {
	liveTotal = 0;
	for (let item of Object.values(totalPaid)) {
		
		liveTotal += item;
	};
	numberDisplayed.innerHTML = "$" + liveTotal;
}

function updateTotal(itmeId, cost) {
	totalPaid[itmeId] = cost;
	console.log(totalPaid)
	updateLiveTotal();
}

function deleteFromtotal(itmeId) {
	delete totalPaid[itmeId];
	updateLiveTotal();
}

window.addEventListener("load", (event) => {
	updateLiveTotal();
});
