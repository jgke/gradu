enum OptionalInt {
    Value(i32),
    Missing,
}

let x = OptionalInt::Value(5);

match x {
    OptionalInt::Value(i) if i > 5 => println!("Got an int > 5!"),
    OptionalInt::Value(..) => println!("Got an int!"),
    OptionalInt::Missing => println!("Empty OptionalInt."),
}
