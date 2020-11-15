function FV(PV,i,n){
	var x=(1+i/100)
	var FV=PV*(Math.pow(x,n))
	return FV;
}

function Cal_FV(){
	var pvalue=parseFloat(document.getElementById("a").value);
	var interest=parseFloat(document.getElementById("b").value);
	var num=parseInt(document.getElementById("c").value);
	var fvalue=FV(pvalue, interest, num);
	var fv=fvalue.toFixed(2);
	document.getElementById('ans').textContent="Montante:  R$"+fv;
}