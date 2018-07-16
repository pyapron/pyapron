#include <stdlib.h>
#include "apron/ap_tcons1.h"

void tcons1_alloc(ap_constyp_t constyp,
                  ap_texpr1_t * texpr1,
                  ap_scalar_t * scalar)
{
    ap_tcons1_t * tcons1 = malloc(sizeof(ap_tcons1_t));
    *tcons1 = ap_tcons1_make(constyp, texpr1, scalar);
}
