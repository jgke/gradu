type Stringer interface {
    String() string
}

func stringify(value interface{}) string {
    switch str := value.(type) {
    case string:
        return str
    case Stringer:
        return str.String()
    default:
        return ""
    }
}
