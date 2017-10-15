const deleteClicked = (id) => {
    deleteURL = `./comments/${id}`
    fetch(deleteURL, {
      method: 'DELETE'
    }).then(() => {
      document.location.reload(true);
    }).catch(function(err) {  
      console.log('Fetch Error :-S', err);  
    });
  }