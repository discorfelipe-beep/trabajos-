const jwt = require('jsonwebtoken');

function verificarToken(req, res, next) {
  const encabezado = req.headers.authorization || '';
  const [tipo, token] = encabezado.split(' ');

  if (tipo !== 'Bearer' || !token) {
    return res.status(401).json({ error: 'Debes iniciar sesión (falta el token)' });
  }

  try {
    // verify revisa la firma y la fecha de expiracion; si algo falla lanza un error
    req.cuenta = jwt.verify(token, process.env.JWT_SECRETO);
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Token inválido o expirado' });
  }
}

module.exports = verificarToken;