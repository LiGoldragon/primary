#![allow(dead_code)]

use std::marker::PhantomData;

trait Phase {
    type At<Position, Literal, Output>;
}

enum Logos {}
enum Nomos {}

impl Phase for Logos {
    type At<Position, Literal, Output> = Output;
}

impl Phase for Nomos {
    type At<Position, Literal, Output> = Slot<Position, Literal, Output>;
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Name(u64);

#[derive(Clone, Debug, PartialEq, Eq)]
enum Visibility {
    Private,
    Public,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum Expr<T> {
    Constant { value: T },
    Choose {
        condition: bool,
        when_true: Box<Expr<T>>,
        when_false: Box<Expr<T>>,
    },
}

impl<T> Expr<T> {
    fn evaluate(self) -> T {
        match self {
            Self::Constant { value } => value,
            Self::Choose {
                condition,
                when_true,
                when_false,
            } => {
                if condition {
                    when_true.evaluate()
                } else {
                    when_false.evaluate()
                }
            }
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Slot<Position, Literal, Output> {
    term: SlotTerm<Literal, Output>,
    position: PhantomData<fn() -> Position>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum SlotTerm<Literal, Output> {
    Literal { value: Literal },
    Evaluate { expression: Expr<Output> },
}

impl<Position, Literal, Output> Slot<Position, Literal, Output> {
    fn literal(value: Literal) -> Self {
        Self {
            term: SlotTerm::Literal { value },
            position: PhantomData,
        }
    }

    fn evaluate(expression: Expr<Output>) -> Self {
        Self {
            term: SlotTerm::Evaluate { expression },
            position: PhantomData,
        }
    }

    fn lower(self, lower_literal: impl FnOnce(Literal) -> Output) -> Output {
        match self.term {
            SlotTerm::Literal { value } => lower_literal(value),
            SlotTerm::Evaluate { expression } => expression.evaluate(),
        }
    }
}

enum RootPosition {}
enum HeaderPosition {}
enum NamePosition {}
enum VisibilityPosition {}
enum BodyPosition {}
enum VariantsPosition {}
enum VariantPosition {}
enum VariantNamePosition {}
enum AliasesPosition {}
enum AliasPosition {}

struct Header<P: Phase> {
    name: P::At<NamePosition, Name, Name>,
    visibility: P::At<VisibilityPosition, Visibility, Visibility>,
}

enum Body<P: Phase> {
    Unit,
    Enumeration {
        variants: P::At<
            VariantsPosition,
            SequenceLiteral<
                P::At<VariantPosition, Variant<P>, Variant<Logos>>,
                Variant<Logos>,
            >,
            Vec<Variant<Logos>>,
        >,
    },
}

struct Variant<P: Phase> {
    name: P::At<VariantNamePosition, Name, Name>,
    aliases: P::At<
        AliasesPosition,
        SequenceLiteral<P::At<AliasPosition, Name, Name>, Name>,
        Vec<Name>,
    >,
}

struct Declaration<P: Phase> {
    header: P::At<HeaderPosition, Header<P>, Header<Logos>>,
    body: P::At<BodyPosition, Body<P>, Body<Logos>>,
}

struct SequenceLiteral<ElementTerm, OutputElement> {
    pieces: Vec<SequencePiece<ElementTerm, OutputElement>>,
}

enum SequencePiece<ElementTerm, OutputElement> {
    Element { value: ElementTerm },
    Splice { expression: Expr<Vec<OutputElement>> },
    Insert {
        index: usize,
        expression: Expr<Vec<OutputElement>>,
    },
}

type NomosRoot = Slot<RootPosition, Declaration<Nomos>, Declaration<Logos>>;

fn lower_header(value: Header<Nomos>) -> Header<Logos> {
    Header {
        name: value.name.lower(|literal| literal),
        visibility: value.visibility.lower(|literal| literal),
    }
}

fn lower_name_sequence(
    value: SequenceLiteral<Slot<AliasPosition, Name, Name>, Name>,
) -> Vec<Name> {
    lower_sequence(value, |element| element.lower(|literal| literal))
}

fn lower_variant(value: Variant<Nomos>) -> Variant<Logos> {
    Variant {
        name: value.name.lower(|literal| literal),
        aliases: value.aliases.lower(lower_name_sequence),
    }
}

fn lower_variant_sequence(
    value: SequenceLiteral<
        Slot<VariantPosition, Variant<Nomos>, Variant<Logos>>,
        Variant<Logos>,
    >,
) -> Vec<Variant<Logos>> {
    lower_sequence(value, |element| element.lower(lower_variant))
}

fn lower_sequence<ElementTerm, OutputElement>(
    value: SequenceLiteral<ElementTerm, OutputElement>,
    mut lower_element: impl FnMut(ElementTerm) -> OutputElement,
) -> Vec<OutputElement> {
    let mut output = Vec::new();
    for piece in value.pieces {
        match piece {
            SequencePiece::Element { value } => output.push(lower_element(value)),
            SequencePiece::Splice { expression } => output.extend(expression.evaluate()),
            SequencePiece::Insert { index, expression } => {
                let inserted = expression.evaluate();
                output.splice(index..index, inserted);
            }
        }
    }
    output
}

fn lower_body(value: Body<Nomos>) -> Body<Logos> {
    match value {
        Body::Unit => Body::Unit,
        Body::Enumeration { variants } => Body::Enumeration {
            variants: variants.lower(lower_variant_sequence),
        },
    }
}

fn lower_declaration(value: Declaration<Nomos>) -> Declaration<Logos> {
    Declaration {
        header: value.header.lower(lower_header),
        body: value.body.lower(lower_body),
    }
}

fn lower_root(value: NomosRoot) -> Declaration<Logos> {
    value.lower(lower_declaration)
}

fn computed_name(value: u64) -> Slot<AliasPosition, Name, Name> {
    Slot::evaluate(Expr::Constant { value: Name(value) })
}

fn main() {
    let nested_aliases = SequenceLiteral {
        pieces: vec![
            SequencePiece::Element {
                value: Slot::literal(Name(30)),
            },
            SequencePiece::Splice {
                expression: Expr::Constant {
                    value: vec![Name(40), Name(50)],
                },
            },
            SequencePiece::Insert {
                index: 1,
                expression: Expr::Constant {
                    value: vec![Name(35)],
                },
            },
            SequencePiece::Element {
                value: computed_name(60),
            },
        ],
    };

    let local_variant = Variant::<Nomos> {
        name: Slot::evaluate(Expr::Constant { value: Name(20) }),
        aliases: Slot::literal(nested_aliases),
    };

    let computed_variant = Variant::<Logos> {
        name: Name(70),
        aliases: vec![Name(80)],
    };

    let nomos = Slot::literal(Declaration::<Nomos> {
        header: Slot::evaluate(Expr::Constant {
            value: Header::<Logos> {
                name: Name(10),
                visibility: Visibility::Public,
            },
        }),
        body: Slot::literal(Body::Enumeration {
            variants: Slot::literal(SequenceLiteral {
                pieces: vec![
                    SequencePiece::Element {
                        value: Slot::literal(local_variant),
                    },
                    SequencePiece::Splice {
                        expression: Expr::Constant {
                            value: vec![computed_variant],
                        },
                    },
                ],
            }),
        }),
    });

    let logos = lower_root(nomos);
    assert_eq!(logos.header.name, Name(10));
    assert_eq!(logos.header.visibility, Visibility::Public);
    let Body::Enumeration { variants } = logos.body else {
        panic!("expected enumeration")
    };
    assert_eq!(variants.len(), 2);
    assert_eq!(variants[0].name, Name(20));
    assert_eq!(
        variants[0].aliases,
        vec![Name(30), Name(35), Name(40), Name(50), Name(60)]
    );
    assert_eq!(variants[1].name, Name(70));

    let computed_sum = Slot::literal(Declaration::<Nomos> {
        header: Slot::literal(Header::<Nomos> {
            name: Slot::literal(Name(90)),
            visibility: Slot::evaluate(Expr::Constant {
                value: Visibility::Private,
            }),
        }),
        body: Slot::evaluate(Expr::Constant { value: Body::Unit }),
    });
    let computed_sum_logos = lower_root(computed_sum);
    assert!(matches!(computed_sum_logos.body, Body::Unit));

    let computed_root = Slot::evaluate(Expr::Constant {
        value: Declaration::<Logos> {
            header: Header::<Logos> {
                name: Name(100),
                visibility: Visibility::Public,
            },
            body: Body::Unit,
        },
    });
    let computed_root_logos = lower_root(computed_root);
    assert_eq!(computed_root_logos.header.name, Name(100));

    println!("phase-family: all position classes lowered without surviving holes");
}
