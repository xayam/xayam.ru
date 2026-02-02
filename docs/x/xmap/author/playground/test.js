
let TC = (function () {
	
	const const1 = "const1";
	class class1 {
		
		constructor(){
			alert("class1");
			
		    alert(const1);
		}
	}
	function func1(){
		alert("func1");
		alert(const1);
		
	   let c = new class1();
	}
	
    return  {func1, class1};
})();

let THREE = (function () {
	const {func1, class1} = TC
    func1();
    let cc = new class1();
	return {func1, class1, cc};
})();

