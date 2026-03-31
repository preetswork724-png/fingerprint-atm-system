console.log('// GA Bank ATM Web App //')
// DISPLAY acc balance -
// allow user to DEPOSIT money (add) -
// alow user to WITHDRAW money (minus) -
// Update BALANCE with every transaction (return sum) -
// make sure the user can't go into NEGATIVE (range) - 
// when balance hits 0 CHANGE BGC -
// LIMIT 10 withdrawls (if less) -

var balance = document.querySelector('.balance');
var inputAmount = document.querySelector('.input-amount');
var withdrawBtn = document.querySelector('.withdraw-btn');
var depositBtn = document.querySelector('.deposit-btn')
var counter = 1;
totalSavings = 20;
balance.textContent = `$ ${totalSavings.toFixed(2)}`;

function depositMoney(amount){
    let newTotal = Number(inputAmount.value) + Number(totalSavings);
            console.log(newTotal)
        totalSavings = newTotal;
            return balance.textContent = `$ ${totalSavings.toFixed(2)}`;
};

function withdrawMoney(amount){
    let newTotal = Number(totalSavings) - Number(inputAmount.value);
            console.log(newTotal)
        totalSavings = newTotal;
        if(newTotal < 0){
            document.querySelector('.warning').textContent = "too low";
            document.querySelector('.warning').style.color = 'red';
        } else if (newTotal == 0) {
            document.querySelector('body').style.backgroundColor = 'red';
            // totalSavings = newTotal;
                return balance.textContent = `$ ${totalSavings.toFixed(2)}`;
        } else if (counter <= 10){
            // totalSavings = newTotal;
                return balance.textContent = `$ ${totalSavings.toFixed(2)}`;
        };
};

function clickLimit(){
    if(counter <= 10 ){
        document.querySelector('.attempts').textContent = `transaction ${counter} of 10`;
        counter++;
    } else{
        document.querySelector('.withdraw-btn').disabled=true;
        document.querySelector('.withdraw-btn').style.color='gray';

    };
};

depositBtn.addEventListener('click', depositMoney);
withdrawBtn.addEventListener('click', withdrawMoney);
withdrawBtn.addEventListener('click', clickLimit)
