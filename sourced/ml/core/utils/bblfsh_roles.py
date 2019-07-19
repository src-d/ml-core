# import bblfsh.compat as bblfsh

# FIXME(guillemdb): The role is no longer an Integer. I hotfixed it matching the roles to the
#  new role name formatting I found inside the nodes. For example: IDENTIFIER -> "Identifier"
#  Otherwise statements like `if bblfsh_roles.IDENTIFIER in node.roles:` will fail because the
#  returned roles are no longer integers but strings.
IDENTIFIER = "Identifier"  # bblfsh.role_id("IDENTIFIER")
QUALIFIED = "Qualified"  # bblfsh.role_id("QUALIFIED")
LITERAL = "Literal"  # bblfsh.role_id("LITERAL")
OPERATOR = "Operator"  # bblfsh.role_id("OPERATOR")
EXPRESSION = "Expression"  # bblfsh.role_id("EXPRESSION")
LEFT = "Left"  # bblfsh.role_id("LEFT")
BINARY = "Binary"  # bblfsh.role_id("BINARY")
ASSIGNMENT = "Assignment"  # bblfsh.role_id("ASSIGNMENT")
FUNCTION = "Function"  # bblfsh.role_id("FUNCTION")
DECLARATION = "Declaration"  # bblfsh.role_id("DECLARATION")
NAME = "Name"  # bblfsh.role_id("NAME")
