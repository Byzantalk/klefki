# Auto-generated by asn1ate v.0.6.0 from signature.asn
# (last modified on 2017-11-19 17:09:45)

from pyasn1.type import univ, char, namedtype, namedval, tag, constraint, useful


class ECDSA_Sig_Value(univ.Sequence):
    pass


ECDSA_Sig_Value.componentType = namedtype.NamedTypes(
    namedtype.NamedType('r', univ.Integer()),
    namedtype.NamedType('s', univ.Integer())
)


