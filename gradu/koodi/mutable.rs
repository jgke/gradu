fn main() {
    let mut a = "Foo".to_string();
    let b = &a;
    a += "bar";
    println!("{}", b);
}
