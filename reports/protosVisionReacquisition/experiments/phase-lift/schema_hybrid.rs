#![allow(dead_code)]

use std::collections::BTreeMap;

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct TypeIdentity(u64);

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct ValueIdentity(u64);

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct EnvironmentKey(u64);

#[derive(Clone, Debug)]
enum Schema {
    Reference { target_type: TypeIdentity },
}

#[derive(Clone, Debug)]
enum RawTemplate {
    LiteralReference {
        claimed_type: TypeIdentity,
        target: ValueIdentity,
    },
    Evaluate {
        claimed_output_type: TypeIdentity,
        key: EnvironmentKey,
    },
}

#[derive(Debug)]
struct SealedTemplate(RawTemplate);

#[derive(Debug)]
struct UncheckedResolved {
    target_type: TypeIdentity,
    target: ValueIdentity,
}

#[derive(Debug)]
struct CheckedResolved(UncheckedResolved);

#[derive(Debug)]
struct LogosReference {
    target: ValueIdentity,
}

#[derive(Default)]
struct World {
    object_types: BTreeMap<ValueIdentity, TypeIdentity>,
}

#[derive(Default)]
struct Environment {
    references: BTreeMap<EnvironmentKey, ValueIdentity>,
}

fn seal_shape(schema: &Schema, raw: RawTemplate) -> Result<SealedTemplate, &'static str> {
    let Schema::Reference { target_type } = schema;
    let claimed = match &raw {
        RawTemplate::LiteralReference { claimed_type, .. } => claimed_type,
        RawTemplate::Evaluate {
            claimed_output_type,
            ..
        } => claimed_output_type,
    };
    if claimed != target_type {
        return Err("expression/literal type does not match its expected position");
    }
    Ok(SealedTemplate(raw))
}

fn evaluate(
    sealed: SealedTemplate,
    environment: &Environment,
) -> Result<UncheckedResolved, &'static str> {
    match sealed.0 {
        RawTemplate::LiteralReference {
            claimed_type,
            target,
        } => Ok(UncheckedResolved {
            target_type: claimed_type,
            target,
        }),
        RawTemplate::Evaluate {
            claimed_output_type,
            key,
        } => {
            let target = environment
                .references
                .get(&key)
                .copied()
                .ok_or("missing environment input")?;
            Ok(UncheckedResolved {
                target_type: claimed_output_type,
                target,
            })
        }
    }
}

fn check_semantics(
    world: &World,
    value: UncheckedResolved,
) -> Result<CheckedResolved, &'static str> {
    match world.object_types.get(&value.target) {
        Some(actual_type) if actual_type == &value.target_type => Ok(CheckedResolved(value)),
        Some(_) => Err("resolved identity has the wrong semantic type"),
        None => Err("resolved identity is absent from the population"),
    }
}

fn reify(value: CheckedResolved) -> LogosReference {
    LogosReference {
        target: value.0.target,
    }
}

fn main() {
    let declaration_type = TypeIdentity(1);
    let schema = Schema::Reference {
        target_type: declaration_type,
    };

    let dangling = seal_shape(
        &schema,
        RawTemplate::LiteralReference {
            claimed_type: declaration_type,
            target: ValueIdentity(999),
        },
    )
    .expect("shape-only sealing deliberately cannot see the population");

    let dangling_resolved = evaluate(dangling, &Environment::default()).unwrap();
    let dangling_error = check_semantics(&World::default(), dangling_resolved).unwrap_err();
    assert_eq!(dangling_error, "resolved identity is absent from the population");

    let target = ValueIdentity(7);
    let key = EnvironmentKey(8);
    let mut world = World::default();
    world.object_types.insert(target, declaration_type);
    let mut environment = Environment::default();
    environment.references.insert(key, target);

    let computed = seal_shape(
        &schema,
        RawTemplate::Evaluate {
            claimed_output_type: declaration_type,
            key,
        },
    )
    .unwrap();
    let checked = check_semantics(&world, evaluate(computed, &environment).unwrap()).unwrap();
    let logos = reify(checked);
    assert_eq!(logos.target, target);

    let wrong_type = seal_shape(
        &schema,
        RawTemplate::Evaluate {
            claimed_output_type: TypeIdentity(2),
            key,
        },
    )
    .unwrap_err();
    assert_eq!(
        wrong_type,
        "expression/literal type does not match its expected position"
    );

    println!("schema-hybrid: shape seal, evaluation, semantic check, typed reification separated");
    println!("counterexample: a shape-valid reference can still be semantically dangling");
}
