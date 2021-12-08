const charactersList = document.getElementById('charactersList');
const searchBar = document.getElementById('searchBar');
let ytChannels = [];
api_key = 'AIzaSyCrIwhrMNtHT0TX7HOJKhuMhWpKHvNjkXM'
//searchBar.addEventListener('keyup', (e) => {
//    const searchString = e.target.value.toLowerCase();

//    const filteredCharacters = ytChannels.filter((character) => {
//        return (
 //           character.name.toLowerCase().includes(searchString) 
//        );
//    });
//    console.log(filteredCharacters);
    //displayCharacters(filteredCharacters);
//});

function getInputValue(){
    // Selecting the input element and get its value 
    var inputVal = document.getElementById("userid").value;
    // Displaying the value
    console.log(inputVal);
}
// Overview and reference for using youtube search: https://developers.google.com/youtube/v3/docs/search
const loadCharacters = async () => {
    try {
        //var forme1 = document.forms.searchform;
        //var formData = new FormData(forme1);
        //var userido = formData.get('userid')
        var ytuserid = document.getElementById("userid").value;
        console.log(ytuserid)
        const res = await fetch("https://www.googleapis.com/youtube/v3/search?part=snippet&key="+api_key+"&t");
        ytChannels = await res.json();
       
        //console.log(channelNames)
        //displayCharacters(channelNames);
    } catch (err) {
        console.error(err);
    }
};

/*const displayCharacters = (channels) => {
    for(channel of channels){
            return `
            <li class="character">
                <h2>${channel}</h2>
            </li>
        `;
        
    }
    charactersList.innerHTML = htmlString;
};
*/
loadCharacters();
