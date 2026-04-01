-- VHDL Test
entity test is
    port (
        clk : in bit;
        q : out bit
    );
end entity;

architecture rtl of test is
begin
    `protect version = 2
`protect encrypt_agent = "Python IEEE 1735 Encryptor"
`protect key_keyowner = "Unknown", key_method = "rsa", key_keyname = "default_key"
`protect key_block
EP359dQrrLvLAzTXwX+IFy3AeX6Q+xNdvm39eTijx6Bid6u9JnbuoeINyKoD9Zgo/R9Tj5Mf8cmdzIeRP9gJAhE8uUa+OkX2yo5UpuggbR4uBgv7JriYStfDdSW6ldbNR5BCGFv0+uoWVBfjQ8g/I1Cb/+3VnHVqz7bvmxkdPjVwgg0o/DoOcuG7P+im6LMl/zKSkL9ggwdSi6rdy1FxwRf9QVbzF7Fz9d0BlPGD02m4g8CWOqha+LF0mxhntXXxEyQKh6CgVjH3GciLm+jiYHN5VH8T/+5Utu1G5YAQKdRFwKWZYOPx13f82Yka1FD4ZwtNurxQ6Lg2bn3eN543Yg==
`protect data_method = "aes256-cbc"
`protect data_block
rT/g1d6bm3iaFlwgFi76bcj5osfDetC6q93Na9qg1wyLsYbMFTbBCqtmU4VsYkOunG9mUni/TLmRBpdenT/JPHMfG9ckfMA21xNF/dfwBoNUuLHFID0fSiY6HL5gThpDzCduQHwQxySU2BcpD4vzHPxjicG0O+/UVlx0f+fCn9Zkwa+FNkF5Yz/c8dzoJRZr
`protect end_protected
end architecture;
