// Ennen makrojen ajamista

macro_rules! impl_from {
    ($Small: ty, $Large: ty) => {
        impl From<$Small> for $Large {
            #[inline]
            fn from(small: $Small) -> $Large {
                small as $Large
            }
        }
    }
}

impl_from!(u16, u32);
impl_from!(u16, u64);

// Makrojen ajamisen jälkeen

impl From<u16> for u32 {
    #[inline]
    fn from(small: u16) -> u32 { small as u32 }
}
impl From<u16> for u64 {
    #[inline]
    fn from(small: u16) -> u64 { small as u64 }
}
