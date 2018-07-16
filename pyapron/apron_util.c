#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <assert.h>
#include "apron/ap_environment.h"
#include "apron/ap_tcons1.h"

ap_tcons1_t * tcons1_alloc(ap_constyp_t constyp,
                           ap_texpr1_t * texpr1,
                           ap_scalar_t * scalar)
{
    ap_tcons1_t * tcons1 = malloc(sizeof(ap_tcons1_t));
    *tcons1 = ap_tcons1_make(constyp, texpr1, scalar);
    return tcons1;
}

ap_texpr1_t * texpr1_var(ap_var_t var)
{
    ap_var_t tmp = var;
    ap_environment_t * env = ap_environment_alloc(&tmp,
                                                  1,
                                                  NULL,
                                                  0);
    assert(env);
    return ap_texpr1_var(env, tmp);
}

ap_environment_t * texpr1_get_env(ap_texpr1_t * texpr1)
{
    return texpr1->env;
}
