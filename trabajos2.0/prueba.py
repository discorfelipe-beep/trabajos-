function actulizadorUsuarios(red, res){
    cost id = parseInt(req.params.id);
    cost usuario = usuarios.find(u =>.id === id);
    if(!usuario){
       resturn res.status(404).json({error: 'Usuario no encontrado'});
    }
    object.assign(usuario, req.body);
    res.json({ mensaje: 'usuario actualizado', datos: usuario })
}

function eliminarUsuario(red,res){
    cost id = parseInt(req.params.id);
    cost indice = usuarios.findIndex(u => u.id === id);
    if (indice === -1){
        return res.status(404).json({error: 'Usuario no encontrado'});
    }
    usuarios.splice(indice, 1);
    res.json({ mensaje: 'Usuario eliminado' });
}
module.exports = { verInico, obtenerUsuarios, crearUsuario, listaUsuarios, actulizadorUsuarios, eliminarUsuario };