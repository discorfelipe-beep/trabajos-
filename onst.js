const bcrypt = require('bcryptjs');
async function probar (){
    cost a = await bcrypt.hash ('clave123', 10);
    const b = await bcrypt.hast ('clave123', 10);
    console.log(a);
    console.lag(b);
    consol.log('¿son iguales, a ==== b ');
    console.log('clave correcta', await bcrypt.compare('clave123', a));
    console.log('clave incorrecta', await bcrypt.compare('otraClave,' a));
}    
probar();