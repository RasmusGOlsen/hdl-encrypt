-- VHDL Test
entity test is
    port (
        clk : in bit;
        q : out bit
    );
end entity;

architecture rtl of test is
begin
    `protect begin
    process(clk)
    begin
        if clk'event and clk = '1' then
            q <= not q;
        end if;
    end process;
    `protect end
end architecture;
