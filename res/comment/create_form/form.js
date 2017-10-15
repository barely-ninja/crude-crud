const makeAPIFunc = (useResult, params = undefined) => {
  const fetchRegionsAPI = (event) => {
    const apiPath = event.target.value ? `./regions/${ event.target.value }` : './regions';
    fetch(apiPath)  
    .then(  
      function(response) {  
        if (response.status !== 200) {  
          console.log('Looks like there was a problem. Status Code: ' +  
            response.status);  
          return;  
        }
        response.json().then(function(data) {
            const opts = data.map((val)=>`<option value="${val.id}">${val.name}</option>`);
            useResult(opts, params);
        });  
      }  
    )  
    .catch(function(err) {  
      console.log('Fetch Error :-S', err);  
    });
  }
  return fetchRegionsAPI; 
}

const insertCityOpts = (opts, params) => {
  document.querySelector('#city_id').innerHTML = opts;
}

const insertRegionOpts = (opts, onChangeFunc) => {
  const regionSelector = document.querySelector('#region_code')
  const chooseReg = '<option value="">Выберите регион...</option>'
  regionSelector.innerHTML = chooseReg+opts;
  regionSelector.onchange=onChangeFunc;            
} 

const cityLoader = makeAPIFunc(insertCityOpts)
const regionLoader = makeAPIFunc(insertRegionOpts, cityLoader)

document.addEventListener('DOMContentLoaded',regionLoader,false);
