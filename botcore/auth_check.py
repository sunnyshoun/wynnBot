TOP = {566698192868212748, 500602166785081344}
MID = {566698192868212748, 500602166785081344}
LOW = {566698192868212748, 500602166785081344}
ENGIN = {566699012489740294}

def check(ctx, permission_list):
    check = 0
    for role in ctx.author.roles:
        if role.id in permission_list:
            check = 1
            break
    return check