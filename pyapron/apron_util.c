#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <assert.h>
#include "apron/ap_tcons1.h"
#include "apron/ap_abstract1.h"

ap_tcons1_t * tcons1_alloc(ap_constyp_t constyp,
                           ap_texpr1_t * texpr1,
                           ap_scalar_t * scalar)
{
    assert(texpr1 != NULL);
    ap_tcons1_t * tcons1 = malloc(sizeof(ap_tcons1_t));
    *tcons1 = ap_tcons1_make(constyp, texpr1, scalar);
    assert(tcons1->tcons0.texpr0 != NULL);
    return tcons1;
}

int get_ap_texpr_add()
{
    return AP_TEXPR_ADD;
}

int get_ap_texpr_sub()
{
    return AP_TEXPR_SUB;
}

int get_ap_texpr_mul()
{
    return AP_TEXPR_MUL;
}

int get_ap_texpr_div()
{
    return AP_TEXPR_DIV;
}

int get_ap_rtype_int()
{
    return AP_RTYPE_INT;
}

int get_ap_rdir_nearest()
{
    return AP_RDIR_NEAREST;
}

int get_ap_cons_eq()
{
    return AP_CONS_EQ;
}

int get_ap_cons_supeq()
{
    return AP_CONS_SUPEQ;
}

int get_ap_cons_sup()
{
    return AP_CONS_SUP;
}

ap_tcons1_array_t * tcons1_array_make(ap_environment_t * env,
                                      size_t size)
{
    ap_tcons1_array_t * arr = malloc(sizeof(ap_tcons1_array_t));
    assert(arr);

    *arr = ap_tcons1_array_make(env, size);

    return arr;
}

ap_environment_t * tcons1_get_env(ap_tcons1_t * tcons1)
{
    return tcons1->env;
}

ap_abstract1_t * abstract1_of_tcons_array(ap_manager_t * aman,
                                          ap_environment_t * env,
                                          ap_tcons1_array_t * array)
{
    ap_abstract1_t * ap_val = malloc(sizeof(ap_abstract1_t));
    assert(ap_val);

    int size = array->tcons0_array.size;

    for(int i = 0; i < size; i++)
    {
        assert(array->tcons0_array.p[i].texpr0 != NULL);
    }

    //*ap_val = ap_abstract1_of_tcons_array(aman, env, array);
    *ap_val = ap_abstract1_bottom(aman, env);

    return ap_val;
}

