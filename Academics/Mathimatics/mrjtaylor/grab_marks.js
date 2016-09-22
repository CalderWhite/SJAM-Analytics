//functions
function mark_package(name,overall){
    this.name = name;
    this.mark = Number(overall);
}
function mean(array){
    var sum = 0;
    for(i=0;i<array.length;i++){
        sum = sum + array[Number(i)];
    }
    var fa = sum / array.length;
    return fa;
}
function median(array){
    array.sort(function(a, b){return b-a});
    var mod = array.length % 2;
    if(mod){
        return array[Math.floor(array.length / 2) + 1];
    }
    else{
        // subtract 1 in the first one since the array is order greatest to least
        return (array[Math.floor(array.length / 2) - 1] + array[(Math.floor(array.length / 2))]) / 2;
    }
}
function collectData(){
    // data/operations
    
    var trs = document.getElementsByTagName("table")[3].children[0].children;
    
    var data = Array.from(trs);
    // now I have to splice some elements from the array, since the table isn't %100 student data
    data.splice(0,3);
    // Data is now an array of all the <tr> elements (that contain student's marks)
    var student_data = [];
    for(var i=0;i<data.length;i++){
        var this_data = data[i];
        if(this_data.children[0].textContent != ""){
            var pkg = new mark_package(this_data.children[0].textContent,this_data.children[1].textContent);
            //console.log(pkg.name);
            student_data.push(pkg);
        }
    }
    // done collecting data
    var numz = [];
    for(i=0;i<student_data.length;i++){
        numz.push(student_data[i].mark);
    }
    return numz;
}
function main(){
    var numz = collectData().sort(function(a, b){return b-a});
    console.log(numz);
    console.log("Mean: " + mean(numz).toString());
    console.log("Median: " + median(numz).toString());
}
main();
