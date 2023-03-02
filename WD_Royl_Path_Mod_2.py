import sys

# Get input and output file names from command-line arguments
if len(sys.argv) < 3:
    print("Usage: python wd_royl_mod02_fast_ram_patch.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Open input and output files
with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
    
    # Read the size of the VSC partition
    f_in.seek(0)
    vsc_size = int.from_bytes(f_in.read(8), byteorder='little')
    
    # Seek to the start of the VSC partition
    f_in.seek(512, 0)
    
    # Read the VSC partition into a buffer
    vsc_data = f_in.read(vsc_size)
    
    # Search for the pattern indicating the location of the ROM data
    pattern = b'\x60\xA0\x94\x00\x01\x00\xD5\x5F\xA9\xAF\xC1\x12\x8D\x03\xB7\xFD'
    offset = vsc_data.find(pattern)
    
    if offset == -1:
        print("Error: ROM data not found.")
        sys.exit(1)
    
    # Calculate the address and size of the ROM data
    rom_addr = 0x100000000 + int.from_bytes(vsc_data[offset+16:offset+20], byteorder='little')
    rom_size = int.from_bytes(vsc_data[offset+20:offset+24], byteorder='little')
    
    # Seek to the start of the ROM data in the VSC partition buffer
    rom_data = vsc_data[offset+24:offset+24+rom_size]
    
    # Write the ROM data to the output file
    f_out.write(rom_data)
    
    # Close the input and output files
    f_in.close()
    f_out.close()
