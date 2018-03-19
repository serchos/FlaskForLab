String.prototype.format = function()
{
  var args = arguments
  return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, i) {
    if (m == "{{") return "{"
    if (m == "}}") return "}"
    return args[i]
  })
}

function isNumeric(n)
{
  return !isNaN(parseFloat(n)) && isFinite(n);
}