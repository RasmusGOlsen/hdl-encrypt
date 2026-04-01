
module top (input clk, input rst, output reg [7:0] count);

    // Normal code
    always @(posedge clk) begin
        if (rst) count <= 0;
    end

    `pragma protect version = 2
`pragma protect encrypt_agent = "Python IEEE 1735 Encryptor"
`pragma protect key_keyowner = "Unknown", key_method = "rsa", key_keyname = "default_key"
`pragma protect key_block
LdIti6G1AHMB0N1b7en2umrjk9ycanbhYfgAcAQgRj/bMf883w/WziA+5wj9IEhGpDDbax+xZVQqEAkh9WdGGIs2BIGsiDmyeu4lrxzftDUPzV9VLN/Rp0A1rtKg1MgTu2fGIMtBlmp6UUQ4bopbyAa0xLzrhTIzKDXVof3jdo6AZYvKIz8Mwjj5T+TUfS6Y6oMdgZKCeeNXTneHSotOLYXB0jRF5IOKmm9YgpbDSJ/QHiyqjF3ZDwlwKBJ068WX/Ltc0X4eC45rVrb9g2ARTGozxqq7HprUUHgFOp/Fw9WAfTZXBNFA0UuTUG4yXhgkThP9ldHl5XXBMxZvCD4r6Q==
`pragma protect data_method = "aes256-cbc"
`pragma protect data_block
2EaQDgpkNwsLv2frfqbHTps72112v9tQ2tK97IirSbIwd8M8Ex+X4roX5FxhOgeouS8yVgV7p9S2/QT30egcNKAcNBJqL0no3a8gima7UfckCpNjWcWun5IgnjyLFbv+GjP8WK8Kab+CAWKFcGA9PA==
`pragma protect end_protected

    // More normal code
    assign some_signal = count[0];

endmodule
