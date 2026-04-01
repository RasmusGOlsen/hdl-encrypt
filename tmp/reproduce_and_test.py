from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate RSA private/public key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Export public key
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

with open("test_key.pub", "wb") as f:
    f.write(public_pem)

# Create a sample Verilog file with pragmas
verilog_content = """
module top (input clk, input rst, output reg [7:0] count);

    // Normal code
    always @(posedge clk) begin
        if (rst) count <= 0;
    end

    `pragma protect begin
    // Secret logic
    always @(posedge clk) begin
        if (!rst) count <= count + 1;
    end
    `pragma protect end

    // More normal code
    assign some_signal = count[0];

endmodule
"""

with open("sample.v", "w") as f:
    f.write(verilog_content)

print("Created test_key.pub and sample.v")
