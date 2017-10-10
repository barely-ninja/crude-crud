document.addEventListener('DOMContentLoaded',function() {
    document.querySelector('select[name="region"]').onchange=changeEventHandler;
},false);

function changeEventHandler(event) {
    const apiPath = `./region/${ event.target.value }`;
    fetch(apiPath)  
    .then(  
      function(response) {  
        if (response.status !== 200) {  
          console.log('Looks like there was a problem. Status Code: ' +  
            response.status);  
          return;  
        }
        response.json().then(function(data) {
            opts = data.map((val)=>`<option value="${val.id}">${val.name}</option>`);
            document.querySelector('select[name="city"]').innerHTML = opts;
            console.log(data);  
        });  
      }  
    )  
    .catch(function(err) {  
      console.log('Fetch Error :-S', err);  
    });
}


