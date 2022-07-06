const view = new Vue({
    el: "#root",
    data: {
        x: 's'
    },
    methods: {
        persianNumber: (number) => {

            const persian = {
                0: "۰", 1: "۱", 2: "۲", 3: "۳", 4: "۴", 5: "۵", 6: "۶", 7: "۷",
                8: "۸", 9: "۹"
            };
            number = number.toString().split("");
            let persianNumber = ""
            for (let i = 0; i < number.length; i++) {
                number[i] = persian[number[i]];
            }
            for (let i = 0; i < number.length; i++) {
                persianNumber += number[i];
            }
            return persianNumber;
        },
        digitsSeprate: (Number) => {
            Number+= '';
            Number= Number.replace(',', '');
            x = Number.split('.');
            y = x[0];
            z= x.length > 1 ? '.' + x[1] : '';
            var rgx = /(\d+)(\d{3})/;
            while (rgx.test(y))
            y= y.replace(rgx, '$1' + ',' + '$2');
            return y+ z;

        }

    }
})