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
    ap_tcons1_t * tcons1 = malloc(sizeof(ap_tcons1_t));
    *tcons1 = ap_tcons1_make(constyp, texpr1, scalar);
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

void tcons1_array_set(ap_tcons1_array_t * array,
                      size_t i,
                      ap_tcons1_t * tcons1)
{
    int res = ap_tcons1_array_set(array, i, tcons1);
    assert(!res);
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

    *ap_val = ap_abstract1_of_tcons_array(aman, env, array);

    return ap_val;
}

ap_environment_t * tcons1_array_env(ap_tcons1_array_t * array)
{
    return array->env;
}

void abstract1_dump(ap_manager_t * man,
                    ap_abstract1_t * val)
{
    ap_abstract1_fprint(stdout, man, val);
}

ap_environment_t * abstract1_env(ap_abstract1_t * val)
{
    return val->env;
}

ap_abstract1_t * abstract1_change_environment(ap_manager_t * man,
                                              ap_abstract1_t * x,
                                              ap_environment_t * env)
{
    ap_abstract1_t * ap_val = malloc(sizeof(ap_abstract1_t));
    assert(ap_val);

    *ap_val = ap_abstract1_change_environment(man, 0, x, env, 0);

    return ap_val;
}

ap_abstract1_t * abstract1_join(ap_manager_t * man,
                                ap_abstract1_t * x1,
                                ap_abstract1_t * x2)
{
    ap_abstract1_t * ap_val = malloc(sizeof(ap_abstract1_t));
    assert(ap_val);

    *ap_val = ap_abstract1_join(man, 0, x1, x2);
    
    return ap_val;
}

ap_abstract1_t * abstract1_meet(ap_manager_t * man,
                                ap_abstract1_t * x1,
                                ap_abstract1_t * x2)
{
    ap_abstract1_t * ap_val = malloc(sizeof(ap_abstract1_t));
    assert(ap_val);

    *ap_val = ap_abstract1_meet(man, 0, x1, x2);
    
    return ap_val;
}

ap_tcons1_array_t * abstract1_to_tcons_array(ap_manager_t * man,
                                             ap_abstract1_t * x)
{
    ap_tcons1_array_t * array = malloc(sizeof(ap_tcons1_array_t));
    assert(array);

    *array = ap_abstract1_to_tcons_array(man, x);

    return array;
}

size_t tcons1_array_size(ap_tcons1_array_t * array)
{
    return ap_tcons1_array_size(array);
}

ap_tcons1_t * tcons1_array_get(ap_tcons1_array_t * array,
                               size_t index)
{
    ap_tcons1_t * tcons1 = malloc(sizeof(ap_tcons1_t));
    assert(tcons1);

    *tcons1 = ap_tcons1_array_get(array, index);

    return tcons1;
}

ap_constyp_t tcons1_constyp(ap_tcons1_t * tcons1)
{
    return *(ap_tcons1_constypref(tcons1));
}

ap_scalar_t * tcons1_scalar(ap_tcons1_t * tcons1)
{
    return ap_tcons1_scalarref(tcons1);
}

ap_abstract1_t * abstract1_assign(ap_manager_t * man,
                                  ap_abstract1_t * x,
                                  ap_var_t var,
                                  ap_texpr1_t * texpr1)
{
    ap_abstract1_t * res = malloc(sizeof(ap_abstract1_t));
    assert(res);

    *res = ap_abstract1_assign_texpr_array(man,
                                           0,
                                           x,
                                           &var,
                                           texpr1,
                                           1,
                                           NULL);
    return res;
}

ap_abstract1_t * abstract1_top(ap_manager_t * man)
{
    ap_abstract1_t * res = malloc(sizeof(ap_abstract1_t));
    assert(res);

    ap_environment_t * empty_env = ap_environment_alloc_empty();
    *res = ap_abstract1_top(man, empty_env);

    return res;
}

ap_abstract1_t * abstract1_bottom(ap_manager_t * man)
{
    ap_abstract1_t * res = malloc(sizeof(ap_abstract1_t));
    assert(res);

    ap_environment_t * empty_env = ap_environment_alloc_empty();
    *res = ap_abstract1_bottom(man, empty_env);

    return res;
}

ap_abstract1_t * abstract1_widening(ap_manager_t * man,
                                    ap_abstract1_t * x1,
                                    ap_abstract1_t * x2)
{
    ap_abstract1_t * ap_val = malloc(sizeof(ap_abstract1_t));
    assert(ap_val);

    *ap_val = ap_abstract1_widening(man, x1, x2);
    
    return ap_val;
}

ap_abstract1_t * abstract1_forget(ap_manager_t * man,
                                  ap_abstract1_t * x,
                                  ap_var_t var)
{
    ap_abstract1_t * ap_val = malloc(sizeof(ap_abstract1_t));
    assert(ap_val);

    *ap_val = ap_abstract1_forget_array(man, 0, x, &var, 1, 0);
    
    return ap_val;
}
