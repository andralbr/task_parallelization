#include <iostream>
#include <cstdlib>
#include <chrono>
#include <thread>
#include <fstream>


int main(int argc, char* argv[])
{
    std::string config;
    if (argc > 1)
        config = std::string(argv[1]);
    std::cout << "Config: " << config << "\n" << std::flush;

    std::this_thread::sleep_for(std::chrono::seconds(10));

    if (const char* env_display = std::getenv("DISPLAY"))
        std::cout << "DISPLAY = " << env_display << "\n" << std::flush;
    else
        std::cout << "DISPLAY unset\n" << std::flush;

    if (const char* env_cuda = std::getenv("CUDA_VISIBLE_DEVICES"))
        std::cout << "CUDA_VISIBLE_DEVICES = " << env_cuda << "\n" << std::flush;
    else
        std::cout << "CUDA_VISIBLE_DEVICES unset\n" << std::flush;

    std::string server_address{"undefined"};        
    if (const char* env_adr = std::getenv("SERVER_ADDRESS"))
    {
        server_address = std::string(env_adr);
        std::cout << "SERVER_ADDRESS = " << env_adr << "\n" << std::flush;
    }
    else
        std::cout << "SERVER_ADDRESS unset\n" << std::flush;       

    //throw std::runtime_error("This did not work!");

    // Write output file
    std::ofstream myfile;
    myfile.open ("output_file.txt");
    myfile << "Config: " << config << "\n";
    myfile << "Server address: " << server_address << "\n";
    myfile.close();  

    std::cerr << "do not worry\n" << std::flush;

    return 0;
}