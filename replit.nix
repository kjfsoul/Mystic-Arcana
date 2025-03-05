{pkgs}: {
  deps = with pkgs; [
    pkgs.lsof
    pkgs.killall
    python310  # Use Python 3.10 to match your .replit configuration
    python310Packages.pip  # For installing Python packages via requirements.txt
  ];
}